<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use AppBundle\Entity\Commune;

class ContribuezController extends Controller
{
	/**
	* @Route("/contribuez", name="contribuez")
	*/
	public function indexAction()
	{
		return $this->render('contribuez/index.html.twig', array());
	}

	/**
	* @Route("/contribuez/histoire", name="contribuezHistoire")
	*/
	public function histoireAction()
	{
		return $this->render('contribuez/histoire.html.twig', array());
	}

	/**
	* @Route("/contribuez/geographie", name="contribuezGeographie")
	*/
	public function geographieAction()
	{
		return $this->render('contribuez/geographie.html.twig', array());
	}

	/**
	* @Route("/contribuez/economie", name="contribuezEconomie")
	*/
	public function economieAction()
	{
		return $this->render('contribuez/economie.html.twig', array());
	}

	/**
	* @Route("/contribuez/population", name="contribuezPopulation")
	*/
	public function populationAction()
	{
		return $this->render('contribuez/population.html.twig', array());
	}

	/**
	* @Route("/contribuez/toponymie", name="contribuezToponymie")
	*/
	public function toponymieAction()
	{
		return $this->render('contribuez/toponymie.html.twig', array());
	}

	/**
	* @Route("/contribuez/politique", name="contribuezPolitique")
	*/
	public function politiqueAction()
	{
		return $this->render('contribuez/politique.html.twig', array());
	}

	/**
	* @Route("/contribuez/culture", name="contribuezCulture")
	*/
	public function cultureAction()
	{
		return $this->render('contribuez/culture.html.twig', array());
	}

	/**
	* @Route("/contribuez/urbanisme", name="contribuezUrbanisme")
	*/
	public function urbanismeAction()
	{
		return $this->render('contribuez/urbanisme.html.twig', array());
	}
}
