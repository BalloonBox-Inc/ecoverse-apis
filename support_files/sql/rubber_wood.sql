
SELECT
    g.GroupSchemeName,
    rmu.RegionalManagerUnitName,
    f.FarmName,
    f.FarmSize,
    area.AreaTypeName,
    mgt.UnitNumber,
    mgt.PolygonArea,
    mgt.EffectiveArea,
    mgt.SphaAge,
    mgt.SphaSurvival,
    mgt.UtilMAI,
    mgt.Survival,
    mgt.PlannedPlantDT,
    mgt.PlantDT,
    mgt.UtilMAI * mgt.EffectiveArea * DATEDIFF(year, mgt.PlantDT, GETDATE()) AS TotalVolume,
    s.SpeciesGroupTemplateName,
    s.GenusName,
    s.SpecieName AS SpeciesName,
    s.ShortCode,
    s.CommonName

FROM fmp.ManagementUnit AS mgt

    LEFT JOIN gs.Farm AS f
    ON mgt.FarmId = f.FarmId

    LEFT JOIN gs.GroupScheme AS g
    ON mgt.GroupSchemeId = g.GroupSchemeId

    LEFT JOIN gs.RegionalManagerUnit as rmu
    ON f.RegionalManagerUnitId = rmu.RegionalManagerUnitId

    LEFT JOIN fmp.AreaType AS area
    ON mgt.AreaTypeId = area.AreaTypeId

    LEFT JOIN (
    SELECT
        a.SpeciesGroupTemplateId,
        a.SpeciesGroupTemplateName,
        b.GenusName,
        b.SpecieName,
        b.ShortCode,
        b.CommonName

    FROM (
        SELECT
            sgt.SpeciesGroupTemplateId,
            sgt.SpeciesGroupTemplateName

        FROM fmp.SpeciesGroupTemplate AS sgt
        ) AS a

        FULL OUTER JOIN (
        SELECT
            sgtsmd.SpeciesGroupTemplateId,
            smd.GenusName,
            smd.SpecieName,
            smd.ShortCode,
            smd.CommonName,
            sgtsmd.Composition

        FROM fmp.SpeciesGroupTemplateSpeciesMasterData AS sgtsmd

            LEFT JOIN fmp.SpeciesMasterData AS smd
            ON sgtsmd.SpeciesMasterDataId = smd.SpeciesMasterDataId
        ) AS b

        ON a.SpeciesGroupTemplateId = b.SpeciesGroupTemplateId
    ) AS s

    ON mgt.SpeciesGroupTemplateId = s.SpeciesGroupTemplateId

WHERE g.GroupSchemeName = 'Sri Trang Thailand'
