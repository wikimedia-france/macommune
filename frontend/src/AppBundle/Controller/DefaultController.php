<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class DefaultController extends Controller
{
	/**
	* @Route("/", name="home")
	*/
	public function indexAction(Request $request)
	{
		return $this->render('index.html.twig', array());
	}

	/**
	* @Route("/api/suggest", name="apiSuggest")
	*/
	public function suggestAction(Request $request)
	{
		$json = json_encode(array(
			array("str" => "plop")
		));
		return new Response($json);
	}
}
