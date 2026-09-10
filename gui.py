#!/usr/bin/env python3
"""
PhasicFlow GUI
GUI for the supplied:
  - writeParticles.py
  - writeMesh.py
  - writeField.py

It writes:
  settings/particlesDict
  system/blockMeshDict
  system/setFieldsDict

Run from the PhasicFlow case directory:
    python3 PhasicFlow_GUI.py
"""

import os
import re
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


CASE = Path.cwd()


class PhasicFlowGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PhasicFlow – Case Setup")
        self.geometry("850x720")
        self.minsize(760, 620)

        # Defaults taken directly from the supplied Python files.
        self.vars = {
            # particles
            "p_distance": tk.StringVar(value="0.005"),
            "p_num": tk.StringVar(value="6"),
            "p_minx": tk.StringVar(value="0.001"),
            "p_miny": tk.StringVar(value="0.002"),
            "p_minz": tk.StringVar(value="0.007"),
            "p_maxx": tk.StringVar(value="0.004"),
            "p_maxy": tk.StringVar(value="0.003"),
            "p_maxz": tk.StringVar(value="0.012"),

            # mesh
            "scale": tk.StringVar(value="0.01"),
            "mesh_x": tk.StringVar(value="0.5"),
            "mesh_y": tk.StringVar(value="0.5"),
            "mesh_z": tk.StringVar(value="1.5"),
            "nx": tk.StringVar(value="10"),
            "ny": tk.StringVar(value="10"),
            "nz": tk.StringVar(value="20"),

            # fluid field
            "c_x": tk.StringVar(value="0.0025"),
            "c_y": tk.StringVar(value="0.0025"),
            "c_z": tk.StringVar(value="0.003"),
            "radius": tk.StringVar(value="0.001"),
        }

        self._build_ui()
        self._update_paths()

    def _build_ui(self):
        header = ttk.Frame(self, padding=12)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="PhasicFlow Case Setup",
            font=("TkDefaultFont", 18, "bold")
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Configure the supplied particle, mesh and setFields generators."
        ).pack(anchor="w", pady=(3, 0))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        particles = ttk.Frame(notebook, padding=15)
        mesh = ttk.Frame(notebook, padding=15)
        field = ttk.Frame(notebook, padding=15)

        notebook.add(particles, text="Particles")
        notebook.add(mesh, text="Mesh")
        notebook.add(field, text="Fluid / Field")

        self._particle_tab(particles)
        self._mesh_tab(mesh)
        self._field_tab(field)

        bottom = ttk.Frame(self, padding=(12, 0, 12, 12))
        bottom.pack(fill="x")

        self.status = ttk.Label(bottom, text="Ready", relief="sunken", anchor="w")
        self.status.pack(fill="x", pady=(0, 7))

        buttons = ttk.Frame(bottom)
        buttons.pack(fill="x")

        ttk.Button(
            buttons, text="Generate Input Files",
            command=self.generate_files
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            buttons, text="Run Particle Test",
            command=self.run_particle_test
        ).pack(side="left", padx=6)

        ttk.Button(
            buttons, text="Run Allrun",
            command=self.run_allrun
        ).pack(side="left", padx=6)

        ttk.Button(
            buttons, text="Clean Case",
            command=self.clean_case
        ).pack(side="left", padx=6)

        ttk.Button(
            buttons, text="Show Generated Files",
            command=self.show_files
        ).pack(side="left", padx=6)

        ttk.Button(
            buttons, text="Exit",
            command=self.destroy
        ).pack(side="right")

        log_frame = ttk.LabelFrame(self, text="Console", padding=8)
        log_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log = tk.Text(log_frame, height=10, wrap="word")
        scroll = ttk.Scrollbar(log_frame, command=self.log.yview)
        self.log.configure(yscrollcommand=scroll.set)
        self.log.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _particle_tab(self, parent):
        self._section(parent, "Ordered particle generation", 0)

        self._entry(parent, "Particle spacing", "p_distance", 1,
                    "Distance used by ordered positioning")
        self._entry(parent, "Number of points", "p_num", 2,
                    "numPoints")

        ttk.Separator(parent).grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)
        ttk.Label(parent, text="Box minimum", font=("TkDefaultFont", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=4
        )
        self._entry(parent, "min X", "p_minx", 5)
        self._entry(parent, "min Y", "p_miny", 6)
        self._entry(parent, "min Z", "p_minz", 7)

        ttk.Label(parent, text="Box maximum", font=("TkDefaultFont", 10, "bold")).grid(
            row=4, column=2, sticky="w", pady=4
        )
        self._entry(parent, "max X", "p_maxx", 5, col=2)
        self._entry(parent, "max Y", "p_maxy", 6, col=2)
        self._entry(parent, "max Z", "p_maxz", 7, col=2)

        ttk.Label(
            parent,
            text="axisOrder is kept as (z x y), regionType is kept as box, and shapeName is sph1.",
            foreground="#555555"
        ).grid(row=9, column=0, columnspan=3, sticky="w", pady=(15, 0))

        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)

    def _mesh_tab(self, parent):
        self._section(parent, "blockMesh geometry", 0)

        self._entry(parent, "Scale", "scale", 1,
                    "blockMeshDict scale")
        self._entry(parent, "Raw X length", "mesh_x", 2,
                    "x coordinate before scale")
        self._entry(parent, "Raw Y length", "mesh_y", 3,
                    "y coordinate before scale")
        self._entry(parent, "Raw Z length", "mesh_z", 4,
                    "z coordinate before scale")

        ttk.Separator(parent).grid(row=5, column=0, columnspan=2, sticky="ew", pady=12)

        self._entry(parent, "Cells X", "nx", 6)
        self._entry(parent, "Cells Y", "ny", 7)
        self._entry(parent, "Cells Z", "nz", 8)

        ttk.Label(
            parent,
            text="The supplied file uses scale=0.01, raw dimensions 0.5 × 0.5 × 1.5, and 10 × 10 × 20 cells.",
            foreground="#555555"
        ).grid(row=10, column=0, columnspan=2, sticky="w", pady=(15, 0))

        parent.columnconfigure(1, weight=1)

    def _field_tab(self, parent):
        self._section(parent, "sphereToCell region", 0)

        self._entry(parent, "Centre X", "c_x", 1)
        self._entry(parent, "Centre Y", "c_y", 2)
        self._entry(parent, "Centre Z", "c_z", 3)
        self._entry(parent, "Radius", "radius", 4)

        ttk.Label(
            parent,
            text="defaultFieldValues keeps alpha.water = 1; the sphere region sets alpha.water = 0.",
            foreground="#555555"
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(15, 0))

        parent.columnconfigure(1, weight=1)

    def _section(self, parent, text, row):
        ttk.Label(parent, text=text, font=("TkDefaultFont", 12, "bold")).grid(
            row=row, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

    def _entry(self, parent, label, key, row, hint="", col=0):
        label_col = col
        entry_col = col + 1
        ttk.Label(parent, text=label).grid(
            row=row, column=label_col, sticky="w", padx=(0, 8), pady=4
        )
        e = ttk.Entry(parent, textvariable=self.vars[key], width=18)
        e.grid(row=row, column=entry_col, sticky="ew", padx=(0, 25), pady=4)
        if hint:
            ttk.Label(parent, text=hint, foreground="#777777").grid(
                row=row, column=entry_col + 1, sticky="w", pady=4
            )
        parent.columnconfigure(entry_col, weight=1)

    def _update_paths(self):
        self.write_particles = CASE / "writeParticles.py"
        self.write_mesh = CASE / "writeMesh.py"
        self.write_field = CASE / "writeField.py"

    def _log(self, text):
        self.log.insert("end", text.rstrip() + "\n")
        self.log.see("end")
        self.update_idletasks()

    def _set_status(self, text):
        self.status.config(text=text)
        self.update_idletasks()

    def _float(self, key):
        try:
            return float(self.vars[key].get())
        except ValueError:
            raise ValueError(f"{key} must be a number.")

    def _int(self, key):
        try:
            value = int(self.vars[key].get())
        except ValueError:
            raise ValueError(f"{key} must be an integer.")
        if value <= 0:
            raise ValueError(f"{key} must be greater than zero.")
        return value

    def validate(self):
        for key in [
            "p_distance", "p_minx", "p_miny", "p_minz",
            "p_maxx", "p_maxy", "p_maxz",
            "scale", "mesh_x", "mesh_y", "mesh_z",
            "c_x", "c_y", "c_z", "radius"
        ]:
            self._float(key)

        self._int("p_num")
        self._int("nx")
        self._int("ny")
        self._int("nz")

        if self._float("p_distance") <= 0:
            raise ValueError("Particle spacing must be greater than zero.")
        if self._float("scale") <= 0:
            raise ValueError("Mesh scale must be greater than zero.")
        if self._float("radius") <= 0:
            raise ValueError("Sphere radius must be greater than zero.")

        mins = [self._float(k) for k in ("p_minx", "p_miny", "p_minz")]
        maxs = [self._float(k) for k in ("p_maxx", "p_maxy", "p_maxz")]
        if any(a >= b for a, b in zip(mins, maxs)):
            raise ValueError("Every particle-box minimum must be smaller than its maximum.")

    def generate_particles(self):
        self.validate()
        settings = CASE / "settings"
        settings.mkdir(parents=True, exist_ok=True)

        text = f"""/* -------------------------------*- C++ -*--------------------------------- *\\
|  phasicFlow File                                                            |
|  copyright: www.cemf.ir                                                     |
\\* ------------------------------------------------------------------------- */

objectName    particlesDict;
objectType    dictionary;
fileFormat    ASCII;

setFields
{{
    defaultValue
    {{
        velocity    realx3    (0 0 0);
        rVelocity   realx3    (0 0 0);
        shapeName   word      sph1;
    }}

    selectors
    {{}}
}}

positionParticles
{{
    method ordered;

    orderedInfo
    {{
        distance {self.vars["p_distance"].get()};
        numPoints {self.vars["p_num"].get()};
        axisOrder (z x y);
    }}

    regionType box;

    boxInfo
    {{
        min ({self.vars["p_minx"].get()} {self.vars["p_miny"].get()} {self.vars["p_minz"].get()});
        max ({self.vars["p_maxx"].get()} {self.vars["p_maxy"].get()} {self.vars["p_maxz"].get()});
    }}
}}
"""
        (settings / "particlesDict").write_text(text)
        return settings / "particlesDict"

    def generate_mesh(self):
        self.validate()
        system = CASE / "system"
        system.mkdir(parents=True, exist_ok=True)

        x = self.vars["mesh_x"].get()
        y = self.vars["mesh_y"].get()
        z = self.vars["mesh_z"].get()

        text = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2412                                 |
|   \\\\  /    A nd           |                                                 |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}

scale   {self.vars["scale"].get()};

vertices
(
    (0   0   0)
    ({x} 0   0)
    ({x} {y} 0)
    (0   {y} 0)
    (0   0   {z})
    ({x} 0   {z})
    ({x} {y} {z})
    (0   {y} {z})
);

blocks
(
    hex (0 1 2 3 4 5 6 7) ({self.vars["nx"].get()} {self.vars["ny"].get()} {self.vars["nz"].get()}) simpleGrading (1 1 1)
);

edges
(
);

boundary
(
    atmosphere
    {{
        type patch;
        faces
        (
            (4 5 6 7)
        );
    }}
    walls
    {{
        type wall;
        faces
        (
            (3 7 6 2)
            (2 6 5 1)
            (1 5 4 0)
            (0 4 7 3)
            (0 3 2 1)
        );
    }}
);

// ************************************************************************* //
"""
        (system / "blockMeshDict").write_text(text)
        return system / "blockMeshDict"

    def generate_field(self):
        self.validate()
        system = CASE / "system"
        system.mkdir(parents=True, exist_ok=True)

        text = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     |                                                 |
|   \\\\  /    A nd           |                                                 |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      setFieldsDict;
}}

defaultFieldValues
(
    volScalarFieldValue alpha.water 1
);

regions
(
    sphereToCell
    {{
        centre ({self.vars["c_x"].get()} {self.vars["c_y"].get()} {self.vars["c_z"].get()});
        radius {self.vars["radius"].get()};
        fieldValues
        (
            volScalarFieldValue alpha.water 0
        );
    }}
);

// ************************************************************************* //
"""
        (system / "setFieldsDict").write_text(text)
        return system / "setFieldsDict"

    def generate_files(self):
        try:
            p = self.generate_particles()
            m = self.generate_mesh()
            f = self.generate_field()

            self._log("Generated:")
            self._log(f"  {p}")
            self._log(f"  {m}")
            self._log(f"  {f}")
            self._set_status("Input files generated successfully.")
            messagebox.showinfo("Success", "PhasicFlow input files were generated.")
        except Exception as exc:
            self._set_status("Generation failed.")
            messagebox.showerror("Input error", str(exc))

    def _run_command(self, command, title):
        def worker():
            self._set_status(f"Running: {title}")
            self._log("\n$ " + " ".join(command))

            try:
                proc = subprocess.Popen(
                    command,
                    cwd=CASE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                for line in proc.stdout:
                    self._log(line)
                rc = proc.wait()

                if rc == 0:
                    self._set_status(f"{title}: completed.")
                    self._log(f"[OK] {title} finished with exit code 0.")
                else:
                    self._set_status(f"{title}: FAILED ({rc}).")
                    self._log(f"[ERROR] {title} failed with exit code {rc}.")
            except FileNotFoundError:
                self._set_status(f"{title}: command not found.")
                self._log(f"[ERROR] Command not found: {command[0]}")
            except Exception as exc:
                self._set_status(f"{title}: error.")
                self._log(f"[ERROR] {exc}")

        threading.Thread(target=worker, daemon=True).start()

    def run_particle_test(self):
        try:
            self.generate_files()
            if not messagebox.askyesno(
                "Particle test",
                "This will remove the existing 0 directory and run blockMesh + particlesPhasicFlow.\n\nContinue?"
            ):
                return

            shutil.rmtree(CASE / "0", ignore_errors=True)

            def worker():
                try:
                    self._set_status("Running particle test...")
                    for command in (["blockMesh"], ["particlesPhasicFlow"]):
                        self._log("\n$ " + " ".join(command))
                        proc = subprocess.Popen(
                            command, cwd=CASE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True, bufsize=1
                        )
                        for line in proc.stdout:
                            self._log(line)
                        rc = proc.wait()
                        if rc != 0:
                            self._set_status(f"{command[0]} failed.")
                            self._log(f"[ERROR] {command[0]} returned {rc}.")
                            return

                    pstruct = CASE / "0" / "pStructure"
                    if pstruct.exists() and pstruct.stat().st_size > 0:
                        self._set_status("Particle test passed: 0/pStructure exists.")
                        self._log("[OK] 0/pStructure exists and is non-empty.")
                        messagebox.showinfo(
                            "Particle test passed",
                            "particlesPhasicFlow completed and 0/pStructure was created."
                        )
                    else:
                        self._set_status("Particle test failed: pStructure missing/empty.")
                        self._log("[ERROR] 0/pStructure is missing or empty.")
                        messagebox.showerror(
                            "Particle test failed",
                            "0/pStructure was not created or is empty."
                        )
                except Exception as exc:
                    self._log(f"[ERROR] {exc}")
                    self._set_status("Particle test error.")

            threading.Thread(target=worker, daemon=True).start()

        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def run_allrun(self):
        allrun = CASE / "Allrun"
        if not allrun.exists():
            messagebox.showerror(
                "Allrun not found",
                "No Allrun file was found in the current case directory."
            )
            return

        if not messagebox.askyesno(
            "Run Allrun",
            "Generate the input files first, then execute ./Allrun?\n\n"
            "Make sure your Allrun stops when particlesPhasicFlow fails."
        ):
            return

        try:
            self.generate_files()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        self._run_command(["bash", "./Allrun"], "Allrun")

    def clean_case(self):
        if not messagebox.askyesno(
            "Clean case",
            "Remove processor* , VTK/, and 0/?"
        ):
            return

        for pattern in ["processor*"]:
            for p in CASE.glob(pattern):
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    try:
                        p.unlink()
                    except FileNotFoundError:
                        pass

        shutil.rmtree(CASE / "VTK", ignore_errors=True)
        shutil.rmtree(CASE / "0", ignore_errors=True)

        self._log("[OK] Removed processor*, VTK/, and 0/.")
        self._set_status("Case cleaned.")

    def show_files(self):
        files = [
            CASE / "settings" / "particlesDict",
            CASE / "system" / "blockMeshDict",
            CASE / "system" / "setFieldsDict",
        ]

        win = tk.Toplevel(self)
        win.title("Generated input files")
        win.geometry("850x650")

        text = tk.Text(win, wrap="none")
        yscroll = ttk.Scrollbar(win, command=text.yview)
        text.configure(yscrollcommand=yscroll.set)

        text.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        for path in files:
            text.insert("end", f"\n===== {path} =====\n")
            if path.exists():
                text.insert("end", path.read_text())
            else:
                text.insert("end", "[file does not exist]\n")

        text.configure(state="disabled")


if __name__ == "__main__":
    app = PhasicFlowGUI()
    app.mainloop()
