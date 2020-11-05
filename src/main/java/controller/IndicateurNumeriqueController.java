package controller;

import io.quarkus.panache.common.Sort;
import model.IndicateurNumerique;

import javax.enterprise.context.ApplicationScoped;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.List;

@Path("/")
@ApplicationScoped
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class IndicateurNumeriqueController {

    /*
    @GET
    public List<IndicateurNumerique> list() {
        return IndicateurNumerique.listAll(Sort.by("nomCommune"));
    }
    */

    @GET
    @Path("commune")
    public IndicateurNumerique getBy(@QueryParam("nom") String nom) {
        IndicateurNumerique indicateur = IndicateurNumerique.findByNomCommune(nom);
        if(indicateur == null) {
            throw new WebApplicationException("Aucun indicateur pour cette commune n'a été trouvé.", 404);
        }
        return indicateur;
    }

    @GET
    @Path("{id}")
    public IndicateurNumerique get(@PathParam("id") Long id) {
        IndicateurNumerique indicateur = IndicateurNumerique.findById(id);
        if(indicateur == null) {
            throw new WebApplicationException("Indicateur d'ID " + id + " non trouvé.", 404);
        }
        return indicateur;
    }

}
