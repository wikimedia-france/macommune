<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\Extension\Core\Type\EmailType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\HttpFoundation\Session\Session;

class DefaultController extends Controller
{
	/**
	* @Route("/", name="home")
	*/
	public function indexAction()
	{
		return $this->render('index.html.twig', array());
	}

	/**
	* @Route("/contact", name="contact")
	*/
	public function contactAction(Request $request)
	{
		$session = new Session();
		
		$data = array();
		if ($session->has("commune_title")) $data['ville'] = $session->get("commune_title");

		$form = $this->createFormBuilder($data)
			->add('nom', TextType::class)
			->add('prenom', TextType::class)
			->add('objet', TextType::class)
			->add('ville', TextType::class)
			->add('pseudo', TextType::class, array("required" => false))
			->add('email', EmailType::class)
			->add('message', TextareaType::class)
			->add('send', SubmitType::class, array("label" => "Envoyer"))
			->getForm();

		$form->handleRequest($request);

		if ($form->isValid()) {
			$data = $form->getData();
			$message = \Swift_Message::newInstance()
				->setSubject($data["objet"])
				->setFrom($data["email"])
				->setTo('nico@picapo.net')
				->setBody($data["message"]);

			$this->get('mailer')->send($message);
		}

		return $this->render('contact.html.twig', array(
			'form' => $form->createView()
		));
	}

	/**
	* @Route("/api/suggest/{tree}", name="apiSuggest")
	*/
	public function suggestAction(Request $request, $tree)
	{
		$str = Commune::computeSuggestStr($request->get("str"));
		$url = "http://localhost:8080/suggest?mode=json&size=12&tree=".urlencode($tree)."&str=".urlencode($str);
		return new Response(file_get_contents($url));
	}
}
