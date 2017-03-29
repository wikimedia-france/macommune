<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Cookie;
use Symfony\Component\Config\Definition\Exception\Exception;
use Symfony\Component\HttpFoundation\Session\Session;

use AppBundle\Entity\Commune;
use Doctrine\ORM\Query\ResultSetMapping;

class CommuneController extends Controller
{
	public function computeSectionsState($importance)
	{
		$stmt = $this->getDoctrine()
			->getManager()
			->getConnection()
			->prepare('SELECT AVG(section_geography) as section_geography, AVG(section_history) as section_history, AVG(section_economy) as section_economy, AVG(section_demographics) as section_demographics, AVG(section_etymology) as section_etymology, AVG(section_governance) as section_governance, AVG(section_culture) as section_culture, AVG(section_infrastructure) as section_infrastructure FROM communes WHERE importance = :importance');  
		$stmt->bindValue('importance', $importance);  
		$stmt->execute();  
		return $stmt->fetchAll();  
	}

	public function renderCommune($commune)
	{
		$session = new Session();
		$session->set("commune_title", $commune->getTitle());
		$session->set("commune_wpTitle", $commune->getWpTitle());
		$session->set("commune_qid", $commune->getQid());
	
		$sectionsState = $this->computeSectionsState($commune->getImportance())[0]; 
	
		$response = $this->render('communes/show.html.twig', array(
			"commune" => $commune,
			"sections" => array(
				"history" => $commune->getSectionHistory() / $sectionsState["section_history"] * 100,
				"geography" => $commune->getSectionGeography() / $sectionsState["section_geography"] * 100,
				"economy" => $commune->getSectionEconomy() / $sectionsState["section_economy"] * 100,
				"demographics" => $commune->getSectionDemographics() / $sectionsState["section_demographics"] * 100,
				"etymology" => $commune->getSectionEtymology() / $sectionsState["section_etymology"] * 100,
				"governance" => $commune->getSectionGovernance() / $sectionsState["section_governance"] * 100,
				"culture" => $commune->getSectionCulture() / $sectionsState["section_culture"] * 100,
				"infrastructure" => $commune->getSectionInfrastructure() / $sectionsState["section_infrastructure"] * 100
			),
		));

		return $response;
	}

	/**
	* @Route("/commune/{qid}/show", name="communeShow")
	*/
	public function showAction(Request $request, $qid)
	{
		$em = $this->getDoctrine();
		$commune = $em->getRepository('AppBundle:Commune')->find($qid);
		if (!$commune) throw $this->createNotFoundException('Pas de commune trouvée pour #'.$qid);
		return $this->renderCommune($commune);
	}

	/**
	* @Route("/commune/search", name="communeSearch")
	*/
	public function indexAction(Request $request)
	{
		$title = $request->get("title");
		$em = $this->getDoctrine();
		$communes = $em->getRepository('AppBundle:Commune')->findByTitle($title);

		if (count($communes) == 0) {
			return $this->render('index.html.twig', array("error" => "Cette commune n’existe pas dans notre base"));
		}
		elseif (count($communes) == 1) {
			$commune = $communes[0];
			return $this->renderCommune($commune);
		}
		else {
			return $this->render('communes/list.html.twig', array("communes" => $communes));
		}
	}
}
