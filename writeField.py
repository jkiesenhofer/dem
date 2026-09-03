content = r"""/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  v2412                                 |
|   \\  /    A nd           | Website:  www.openfoam.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      setFieldsDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

defaultFieldValues
(
    volScalarFieldValue alpha.water 1
);

regions
(
    /*boxToCell
    {
        box (0 0 0) (0.5 0.5 0.45);
        fieldValues
        (
            volScalarFieldValue alpha.water 1
        );
    }*/

    sphereToCell
    {
        centre (0.0025 0.0025 0.003);
        radius 0.001; // Adjust this radius value as needed
        fieldValues
        (
            volScalarFieldValue alpha.water 0
        );
    }


);


// ************************************************************************* //
"""

with open("system/setFieldsDict", "w") as f:
    f.write(content)
