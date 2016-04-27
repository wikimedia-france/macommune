<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Cookie;
use Symfony\Component\Config\Definition\Exception\Exception; 
use AppBundle\Entity\Commune;

class CommuneController extends Controller
{
	/**
	* @Route("/commune/{id}/show", name="communeShow")
	*/
	public function showAction(Request $request, $id)
	{
		$em = $this->getDoctrine();
		$commune = $em->getRepository('AppBundle:Commune')->find($id);
		if (!$commune) throw $this->createNotFoundException('Pas de commune trouvée pour #'.$id);
		return $this->render('communes/show.html.twig', array("commune" => $commune));
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
			$response = $this->render('communes/show.html.twig', array("commune" => $commune));
			$response->headers->setCookie(new Cookie('commune_id', $commune->getId(), 0, ""));
			$response->headers->setCookie(new Cookie('commune_title', $commune->getTitle(), 0, ""));
			return $response;
		}
		else {
			return $this->render('communes/list.html.twig', array("communes" => $communes));
		}
	}
}
