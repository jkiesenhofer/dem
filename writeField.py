content = r"""/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  v2412                                 |
|   \\  /    A nd           | Website:  www.openfoam.com                  |
|    \\/     M manipulation |                                                 |
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
    sphereToCell
    {
        centre (0.3 0.3 0.65);
        radius 0.05;
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
