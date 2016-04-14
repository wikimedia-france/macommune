<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Config\Definition\Exception\Exception; 
use AppBundle\Entity\Commune;

class CommuneController extends Controller
{
	/**
	* @Route("/commune", name="communeSearch")
	*/
	public function indexAction(Request $request)
	{
		$search = $request->get("search");
		$em = $this->getDoctrine();
		$communes = $em->getRepository('AppBundle:Commune')->findByTitle($search);

		if (count($communes) == 0) {
			return $this->render('communes/notfound.html.twig', array());
		}
		elseif (count($communes) == 1) {
			return $this->render('communes/show.html.twig', array("commune" => $communes[0]));
		}
		else {
			return $this->render('communes/list.html.twig', array("communes" => $communes));
		}
	}
}
