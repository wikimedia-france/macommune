<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * Commune
 *
 * @ORM\Table(name="communes")
 * @ORM\Entity
 */
class Commune
{
    /**
     * @var string
     *
     * @ORM\Column(name="qid", type="string", length=16, precision=0, scale=0, nullable=false, unique=false)
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="NONE")
     */
    private $qid;

    /**
     * @var string
     *
     * @ORM\Column(name="title", type="string", length=64, precision=0, scale=0, nullable=false, unique=false)
     */
    private $title;

    /**
     * @var string
     *
     * @ORM\Column(name="wp_title", type="string", length=64, precision=0, scale=0, nullable=false, unique=false)
     */
    private $wpTitle;

    /**
     * @var string
     *
     * @ORM\Column(name="suggest_str", type="string", length=64, precision=0, scale=0, nullable=false, unique=false)
     */
    private $suggestStr;

    /**
     * @var string
     *
     * @ORM\Column(name="insee", type="string", length=16, precision=0, scale=0, nullable=false, unique=false)
     */
    private $insee;

    /**
     * @var integer
     *
     * @ORM\Column(name="population", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $population;

    /**
     * @var string
     *
     * @ORM\Column(name="badge", type="string", length=20, precision=0, scale=0, nullable=true, unique=false)
     */
    private $badge;

    /**
     * @var string
     *
     * @ORM\Column(name="progress", type="string", length=20, precision=0, scale=0, nullable=true, unique=false)
     */
    private $progress;

    /**
     * @var string
     *
     * @ORM\Column(name="importance", type="string", length=20, precision=0, scale=0, nullable=true, unique=false)
     */
    private $importance;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_geography", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_geography;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_history", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_history;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_economy", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_economy;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_demographics", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_demographics;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_etymology", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_etymology;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_governance", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_governance;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_culture", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_culture;

    /**
     * @var integer
     *
     * @ORM\Column(name="section_infrastructure", type="integer", precision=0, scale=0, nullable=true, unique=false)
     */
    private $section_infrastructure;

    /**
     * @var \Doctrine\Common\Collections\Collection
     *
     * @ORM\OneToMany(targetEntity="AppBundle\Entity\Section", mappedBy="commune")
     */
    private $sections;

    /**
     * Constructor
     */
    public function __construct()
    {
        $this->sections = new \Doctrine\Common\Collections\ArrayCollection();
    }


    /**
     * Set qid
     *
     * @param string $qid
     *
     * @return Commune
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
     * @return Commune
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
     * Set wpTitle
     *
     * @param string $wpTitle
     *
     * @return Commune
     */
    public function setWpTitle($wpTitle)
    {
        $this->wpTitle = $wpTitle;

        return $this;
    }

    /**
     * Get wpTitle
     *
     * @return string
     */
    public function getWpTitle()
    {
        return $this->wpTitle;
    }

    /**
     * Set suggestStr
     *
     * @param string $suggestStr
     *
     * @return Commune
     */
    public function setSuggestStr($suggestStr)
    {
        $this->suggestStr = $suggestStr;

        return $this;
    }

    /**
     * Get suggestStr
     *
     * @return string
     */
    public function getSuggestStr()
    {
        return $this->suggestStr;
    }

    /**
     * Set insee
     *
     * @param string $insee
     *
     * @return Commune
     */
    public function setInsee($insee)
    {
        $this->insee = $insee;

        return $this;
    }

    /**
     * Get insee
     *
     * @return string
     */
    public function getInsee()
    {
        return $this->insee;
    }

    /**
     * Set population
     *
     * @param integer $population
     *
     * @return Commune
     */
    public function setPopulation($population)
    {
        $this->population = $population;

        return $this;
    }

    /**
     * Get population
     *
     * @return integer
     */
    public function getPopulation()
    {
        return $this->population;
    }

    /**
     * Set badge
     *
     * @param string $badge
     *
     * @return Commune
     */
    public function setBadge($badge)
    {
        $this->badge = $badge;

        return $this;
    }

    /**
     * Get badge
     *
     * @return string
     */
    public function getBadge()
    {
        return $this->badge;
    }

    /**
     * Set progress
     *
     * @param string $progress
     *
     * @return Commune
     */
    public function setProgress($progress)
    {
        $this->progress = $progress;

        return $this;
    }

    /**
     * Get progress
     *
     * @return string
     */
    public function getProgress()
    {
        return $this->progress;
    }

    /**
     * Set importance
     *
     * @param string $importance
     *
     * @return Commune
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

    /**
     * Set section_history
     *
     * @param integer $section_history
     *
     * @return Commune
     */
    public function setSectionHistory($section_history)
    {
        $this->section_history = $section_history;

        return $this;
    }

    /**
     * Get section_history
     *
     * @return integer
     */
    public function getSectionHistory()
    {
        return $this->section_history;
    }

    /**
     * Set section_geography
     *
     * @param integer $section_geography
     *
     * @return Commune
     */
    public function setSectionGeography($section_geography)
    {
        $this->section_ = $section_geography;

        return $this;
    }

    /**
     * Get section_geography
     *
     * @return integer
     */
    public function getSectionGeography()
    {
        return $this->section_geography;
    }

    /**
     * Set section_economy
     *
     * @param integer $section_economy
     *
     * @return Commune
     */
    public function setSectionEconomy($section_economy)
    {
        $this->section_economy = $section_economy;

        return $this;
    }

    /**
     * Get section_economy
     *
     * @return integer
     */
    public function getSectionEconomy()
    {
        return $this->section_economy;
    }

    /**
     * Set section_demographics
     *
     * @param integer $section_demographics
     *
     * @return Commune
     */
    public function setSectionDemographics($section_demographics)
    {
        $this->section_demographics = $section_demographics;

        return $this;
    }

    /**
     * Get section_demographics
     *
     * @return integer
     */
    public function getSectionDemographics()
    {
        return $this->section_demographics;
    }

    /**
     * Set section_etymology
     *
     * @param integer $section_etymology
     *
     * @return Commune
     */
    public function setSectionEtymology($section_etymology)
    {
        $this->section_etymology = $section_etymology;

        return $this;
    }

    /**
     * Get section_etymology
     *
     * @return integer
     */
    public function getSectionEtymology()
    {
        return $this->section_etymology;
    }

    /**
     * Set section_governance
     *
     * @param integer $section_governance
     *
     * @return Commune
     */
    public function setSectionGovernance($section_governance)
    {
        $this->section_governance = $section_governance;

        return $this;
    }

    /**
     * Get section_governance
     *
     * @return integer
     */
    public function getSectionGovernance()
    {
        return $this->section_governance;
    }

    /**
     * Set section_culture
     *
     * @param integer $section_culture
     *
     * @return Commune
     */
    public function setSectionCulture($section_culture)
    {
        $this->section_culture = $section_culture;

        return $this;
    }

    /**
     * Get section_culture
     *
     * @return integer
     */
    public function getSectionCulture()
    {
        return $this->section_culture;
    }

    /**
     * Set section_infrastructure
     *
     * @param integer $section_infrastructure
     *
     * @return Commune
     */
    public function setSectionInfrastructure($section_infrastructure)
    {
        $this->section_infrastructure = $section_infrastructure;

        return $this;
    }

    /**
     * Get section_infrastructure
     *
     * @return integer
     */
    public function getSectionInfrastructure()
    {
        return $this->section_infrastructure;
    }

    /**
     * Add section
     *
     * @param \AppBundle\Entity\Section $section
     *
     * @return Commune
     */
    public function addSection(\AppBundle\Entity\Section $section)
    {
        $this->sections[] = $section;

        return $this;
    }

    /**
     * Remove section
     *
     * @param \AppBundle\Entity\Section $section
     */
    public function removeSection(\AppBundle\Entity\Section $section)
    {
        $this->sections->removeElement($section);
    }

    /**
     * Get sections
     *
     * @return \Doctrine\Common\Collections\Collection
     */
    public function getSections()
    {
        return $this->sections;
    }
}
