content = r"""/* -------------------------------*- C++ -*--------------------------------- *\
|  phasicFlow File                                                            |
|  copyright: www.cemf.ir                                                     |
\* ------------------------------------------------------------------------- */

objectName 	particlesDict;
objectType 	dictionary;
fileFormat 	ASCII;

setFields
{
	defaultValue
	{
		velocity 		realx3 	(0 0 0); 	// linear velocity (m/s)
		rVelocity 		realx3 	(0 0 0);  	// rotational velocity (rad/s)
		shapeName 		word	sph1; 		// name of the particle shape
	}

	selectors
	{}
}


positionParticles
{
    method ordered;

    orderedInfo
    {
        distance   0.0001;           // minimum space between centers of particles
        
        numPoints  6;          // number of particles in the simulation 
        
        axisOrder  (z x y);         // axis order for filling the space with particles
    }

    regionType cylinder;            // other options: box and sphere    

    cylinderInfo                    // cylinder for positioning particles 
    {
        p1     (0.004 0.004 0.012);    // lower corner point of the box 
        
        p2     (0.003 0.003  0.007);    // upper corner point of the box 
        
        radius 0.001;               // radius of cylinder 
    }
}


"""

with open("settings/particlesDict", "w") as f:
    f.write(content)
