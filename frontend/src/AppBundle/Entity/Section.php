<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * Section
 *
 * @ORM\Table(name="sections")
 * @ORM\Entity
 */
class Section
{
    /**
     * @var integer
     *
     * @ORM\Column(name="id", type="integer", length=16, precision=0, scale=0, nullable=false, unique=false)
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="IDENTITY")
     */
    private $id;

    /**
     * @var string
     *
     * @ORM\Column(name="title", type="string", length=64, precision=0, scale=0, nullable=false, unique=false)
     */
    private $title;

    /**
     * @var integer
     *
     * @ORM\Column(name="size", type="integer", precision=0, scale=0, nullable=false, unique=false)
     */
    private $size;

    /**
     * @var boolean
     *
     * @ORM\Column(name="has_sub_article", type="boolean", precision=0, scale=0, nullable=false, unique=false)
     */
    private $hasSubArticle;

    /**
     * @var \AppBundle\Entity\Commune
     *
     * @ORM\ManyToOne(targetEntity="AppBundle\Entity\Commune")
     * @ORM\JoinColumns({
     *   @ORM\JoinColumn(name="qid", referencedColumnName="qid", nullable=true)
     * })
     */
    private $commune;



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
