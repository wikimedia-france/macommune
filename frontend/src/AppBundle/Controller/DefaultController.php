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
	* @Route("/api/suggest/{tree}", name="apiSuggest")
	*/
	public function suggestAction(Request $request, $tree)
	{
		$str = $request->get("str");
		$url = "http://localhost:8080/suggest?mode=json&size=12&tree=".urlencode($tree)."&str=".urlencode($str);
		return new Response(file_get_contents($url));
	}
}
