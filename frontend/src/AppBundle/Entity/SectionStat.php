<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * SectionStat
 *
 * @ORM\Table(name="section_stats")
 * @ORM\Entity
 */
class SectionStat
{
    /**
     * @var integer
     *
     * @ORM\Column(name="id", type="integer", precision=0, scale=0, nullable=false, unique=false)
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="IDENTITY")
     */
    private $id;

    /**
     * @var string
     *
     * @ORM\Column(name="section_title", type="string", length=64, precision=0, scale=0, nullable=false, unique=false)
     */
    private $section_title;

    /**
     * @var integer
     *
     * @ORM\Column(name="mean_size", type="integer", precision=0, scale=0, nullable=false, unique=false)
     */
    private $mean_size;

    /**
     * @var string
     *
     * @ORM\Column(name="importance", type="string", length=20, precision=0, scale=0, nullable=true, unique=false)
     */
    private $importance;



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
     * Set sectionTitle
     *
     * @param string $sectionTitle
     *
     * @return SectionStat
     */
    public function setSectionTitle($sectionTitle)
    {
        $this->section_title = $sectionTitle;

        return $this;
    }

    /**
     * Get sectionTitle
     *
     * @return string
     */
    public function getSectionTitle()
    {
        return $this->section_title;
    }

    /**
     * Set meanSize
     *
     * @param integer $meanSize
     *
     * @return SectionStat
     */
    public function setMeanSize($meanSize)
    {
        $this->mean_size = $meanSize;

        return $this;
    }

    /**
     * Get meanSize
     *
     * @return integer
     */
    public function getMeanSize()
    {
        return $this->mean_size;
    }

    /**
     * Set importance
     *
     * @param string $importance
     *
     * @return SectionStat
     */
    public function setImportance($importance)
    {
        $this->importance = $importance;

        return $this;
    }

    /**
     * Get importance
     *
     * @return string
     */
    public function getImportance()
    {
        return $this->importance;
    }
}
