SELECT
    -- fmp.ManagementUnit
    m.UnitNumber,
    m.EffectiveArea,
    m.PlantDT,
    DATEDIFF(day, m.PlantDT, GETDATE())/365.0 AS PlantAge,
    m.SphaSurvival,
    -- gs.Farm
    f.FarmId,
    f.Latitude,
    f.Longitude,
    f.Province,
    f.FarmSize,
    -- gs.GroupScheme
    g.GroupSchemeName AS GroupScheme,
    -- fmp.ProductGroupTemplate
    p.ProductGroupTemplateDescription AS ProductGroup,
    s.GenusName,
    s.SpecieName AS SpeciesName

FROM fmp.ManagementUnit AS m

    LEFT JOIN gs.Farm AS f
    ON m.FarmId = f.FarmId

    LEFT JOIN gs.GroupScheme AS g
    ON m.GroupSchemeId = g.GroupSchemeId

    LEFT JOIN fmp.ProductGroupTemplate as p
    ON m.ProductGroupTemplateId = p.ProductGroupTemplateId


    LEFT JOIN (
    SELECT
        a.SpeciesGroupTemplateId,
        b.GenusName,
        b.SpecieName

    FROM (
        SELECT
            sgt.SpeciesGroupTemplateId

        FROM fmp.SpeciesGroupTemplate AS sgt
        ) AS a

        FULL OUTER JOIN (
        SELECT
            sgtsmd.SpeciesGroupTemplateId,
            smd.GenusName,
            smd.SpecieName,
            sgtsmd.Composition

        FROM fmp.SpeciesGroupTemplateSpeciesMasterData AS sgtsmd

            LEFT JOIN fmp.SpeciesMasterData AS smd
            ON sgtsmd.SpeciesMasterDataId = smd.SpeciesMasterDataId
        ) AS b
        ON a.SpeciesGroupTemplateId = b.SpeciesGroupTemplateId
    ) AS s
    ON m.SpeciesGroupTemplateId = s.SpeciesGroupTemplateId

WHERE m.PlantDT IS NOT NULL
    AND s.GenusName IS NOT NULL
    AND s.SpecieName IS NOT NULL
    AND f.Latitude != 0
    AND f.Longitude != 0
    AND f.IsSuspended = 'False'
    AND f.IsActive = 'True'
    AND f.FarmId = '{}'




