<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class AgissezController extends Controller
{
	/**
	* @Route("/agissez", name="agissez")
	*/
	public function indexAction()
	{
		return $this->render('agissez/index.html.twig', array());
	}

	/**
	* @Route("/agissez/acteurs", name="agissezActeurs")
	*/
	public function acteursAction()
	{
		return $this->render('agissez/index.html.twig', array());
	}

	/**
	* @Route("/agissez/collectivites", name="agissezCollectivites")
	*/
	public function collectivitesAction()
	{
		return $this->render('agissez/index.html.twig', array());
	}

	/**
	* @Route("/agissez/mediation", name="agissezMediation")
	*/
	public function mediationAction()
	{
		return $this->render('agissez/index.html.twig', array());
	}

	/**
	* @Route("/agissez/enseignants", name="agissezEnseignants")
	*/
	public function enseignantsAction()
	{
		return $this->render('agissez/index.html.twig', array());
	}

	/**
	* @Route("/agissez/associations", name="agissezAssociations")
	*/
	public function associationsAction()
	{
		return $this->render('agissez/index.html.twig', array());
	}
}
