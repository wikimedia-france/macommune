<?php

namespace AppBundle\DataFixtures\ORM;

use Doctrine\Common\DataFixtures\FixtureInterface;
use Doctrine\Common\Persistence\ObjectManager;
use AppBundle\Entity\Commune;

class LoadCommunesData implements FixtureInterface
{
	public function load(ObjectManager $manager)
	{
		$conn = $manager->getConnection()->prepare('SET autocommit=0;')->execute();

		$path = "var/france-communes-data.csv";

		$handle = fopen($path, "r");
		if (!$handle)
			return false;


		$i = 0;
		while (($cells = fgetcsv($handle, 1024, ",", '"')) !== FALSE) {
			if (count($cells) == 4) {
				list($qid, $wp_title, $title, $insee) = $cells;
				$commune = new Commune();
				$commune->setQid($qid);
				$commune->setWpTitle($wp_title);
				$commune->setTitle($title);
				$commune->setInsee($insee);
				$commune->setSuggestStr(Commune::computeSuggestStr($title));

				$manager->persist($commune);
				$manager->flush();
				$manager->clear();

				echo "\r".(++$i);
				flush();
			}
		}
		echo "\n";
	}
}
