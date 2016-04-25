<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use AppBundle\Entity\Commune;

class IllustrezController extends Controller
{
	/**
	* @Route("/illustrez", name="illustrez")
	*/
	public function indexAction()
	{
		return $this->render('illustrez/index.html.twig', array());
	}

	/**
	* @Route("/illustrez/photos", name="illustrezPhotos")
	*/
	public function photosAction()
	{
		return $this->render('illustrez/index.html.twig', array());
	}

	/**
	* @Route("/illustrez/archives", name="illustrezArchives")
	*/
	public function archivesAction()
	{
		return $this->render('illustrez/index.html.twig', array());
	}

	/**
	* @Route("/illustrez/sonore", name="illustrezSonore")
	*/
	public function sonoreAction()
	{
		return $this->render('illustrez/index.html.twig', array());
	}
}
