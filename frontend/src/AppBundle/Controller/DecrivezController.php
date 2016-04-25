<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use AppBundle\Entity\Commune;

class DecrivezController extends Controller
{
	/**
	* @Route("/decrivez", name="decrivez")
	*/
	public function indexAction()
	{
		return $this->render('decrivez/index.html.twig', array());
	}

	/**
	* @Route("/decrivez/histoire", name="decrivezHistoire")
	*/
	public function histoireAction()
	{
		return $this->render('decrivez/histoire.html.twig', array());
	}

	/**
	* @Route("/decrivez/geographie", name="decrivezGeographie")
	*/
	public function geographieAction()
	{
		return $this->render('decrivez/geographie.html.twig', array());
	}

	/**
	* @Route("/decrivez/economie", name="decrivezEconomie")
	*/
	public function economieAction()
	{
		return $this->render('decrivez/economie.html.twig', array());
	}

	/**
	* @Route("/decrivez/population", name="decrivezPopulation")
	*/
	public function populationAction()
	{
		return $this->render('decrivez/population.html.twig', array());
	}

	/**
	* @Route("/decrivez/toponymie", name="decrivezToponymie")
	*/
	public function toponymieAction()
	{
		return $this->render('decrivez/toponymie.html.twig', array());
	}

	/**
	* @Route("/decrivez/politique", name="decrivezPolitique")
	*/
	public function politiqueAction()
	{
		return $this->render('decrivez/politique.html.twig', array());
	}

	/**
	* @Route("/decrivez/culture", name="decrivezCulture")
	*/
	public function cultureAction()
	{
		return $this->render('decrivez/culture.html.twig', array());
	}

	/**
	* @Route("/decrivez/urbanisme", name="decrivezUrbanisme")
	*/
	public function urbanismeAction()
	{
		return $this->render('decrivez/urbanisme.html.twig', array());
	}
}
