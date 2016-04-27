<?php
namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table(name="section")
 */

class Section
{
	/**
	 * @ORM\Column(type="integer", length=16)
	 * @ORM\Id
	 * @ORM\GeneratedValue(strategy="AUTO")
	 */
	protected $id;

	/**
	 * @ORM\ManyToOne(targetEntity="Commune")
	 * @ORM\JoinColumn(name="qid", referencedColumnName="qid")
	 */
	protected $commune;

	/**
	 * @ORM\Column(type="string", length=64)
	 */
	protected $title;

	/**
	 * @ORM\Column(type="integer")
	 */
	protected $size;

	/**
	 * @ORM\Column(type="boolean")
	 */
	protected $hasSubArticle;


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
     * Set qid
     *
     * @param string $qid
     *
     * @return Section
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

    /**
     * Set title
     *
     * @param string $title
     *
     * @return Section
     */
    public function setTitle($title)
    {
        $this->title = $title;

        return $this;
    }

    /**
     * Get title
     *
     * @return string
     */
    public function getTitle()
    {
        return $this->title;
    }

    /**
     * Set size
     *
     * @param integer $size
     *
     * @return Section
     */
    public function setSize($size)
    {
        $this->size = $size;

        return $this;
    }

    /**
     * Get size
     *
     * @return integer
     */
    public function getSize()
    {
        return $this->size;
    }

    /**
     * Set hasSubArticle
     *
     * @param boolean $hasSubArticle
     *
     * @return Section
     */
    public function setHasSubArticle($hasSubArticle)
    {
        $this->hasSubArticle = $hasSubArticle;

        return $this;
    }

    /**
     * Get hasSubArticle
     *
     * @return boolean
     */
    public function getHasSubArticle()
    {
        return $this->hasSubArticle;
    }

    /**
     * Set commune
     *
     * @param \AppBundle\Entity\Commune $commune
     *
     * @return Section
     */
    public function setCommune(\AppBundle\Entity\Commune $commune = null)
    {
        $this->commune = $commune;

        return $this;
    }

    /**
     * Get commune
     *
     * @return \AppBundle\Entity\Commune
     */
    public function getCommune()
    {
        return $this->commune;
    }
}
