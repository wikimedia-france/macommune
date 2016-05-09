<?php
namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table(name="aliases")
 */

class Alias
{
	/**
	 * @ORM\Column(type="integer")
	 * @ORM\Id
	 * @ORM\GeneratedValue(strategy="AUTO")
	 */
	protected $id;

	/**
	 * @ORM\Column(type="string", length=64)
	 */
	protected $alias;

	/**
	 * @ORM\Column(type="string", length=16)
	 */
	protected $qid;

	/**
	 * Get id
	 *
	 * @return integer
	 */
	public function getId()
	{
		return $this->id;
	}

	/**
	 * Set alias
	 *
	 * @param string $alias
	 *
	 * @return Alias
	 */
	public function setAlias($alias)
	{
		$this->alias = $alias;

		return $this;
	}

	/**
	 * Get alias
	 *
	 * @return string
	 */
	public function getAlias()
	{
		return $this->alias;
	}

	/**
	 * Set qid
	 *
	 * @param string $qid
	 *
	 * @return Alias
	 */
	public function setQid($qid)
	{
		$this->qid = $qid;

		return $this;
	}

	/**
	 * Get qid
	 *
	 * @return string
	 */
	public function getQid()
	{
		return $this->qid;
	}
}
