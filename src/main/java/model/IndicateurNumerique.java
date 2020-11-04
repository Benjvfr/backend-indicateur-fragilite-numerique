package model;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

import javax.persistence.Entity;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Entity
public class IndicateurNumerique extends PanacheEntity {

    @NotBlank
    public String nomIris;

    @NotBlank
    public String nomCommune;

    @NotBlank
    public String nomRegion;

    // Scores calculés avec pour référence Region
    @NotNull
    @PositiveOrZero
    public Double scoreAccesInformationRegion;

    @NotNull
    @PositiveOrZero
    public Double scoreAccesInterfaceNumeriqueRegion;

    @NotNull
    @PositiveOrZero
    public Double scoreCapaciteNumeriqueRegion;

    @NotNull
    @PositiveOrZero
    public Double scoreCompetencesAdministrativesRegion;

    // Scores calculés avec pour référence Departement
    @NotNull
    @PositiveOrZero
    public Double scoreAccesInformationDepartement;

    @NotNull
    @PositiveOrZero
    public Double scoreAccesInterfaceNumeriqueDepartement;

    @NotNull
    @PositiveOrZero
    public Double scoreCapaciteNumeriqueDepartement;

    @NotNull
    @PositiveOrZero
    public Double scoreCompetencesAdministrativesDepartement;

    public static IndicateurNumerique findByNomCommune(String nom) {
        return find("nomCommune", nom).firstResult();
    }
}
