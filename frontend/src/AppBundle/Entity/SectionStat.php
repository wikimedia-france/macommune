<?php
namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table(name="section_stats")
 */

class SectionStat
{
	/**
	 * @ORM\Column(type="integer", length=16)
	 * @ORM\Id
	 * @ORM\GeneratedValue(strategy="AUTO")
	 */
	protected $id;

	/**
	 * @ORM\Column(type="string", length=64)
	 */
	protected $section_title;

	/**
	 * @ORM\Column(type="integer")
	 */
	protected $mean_size;

	/**
	 * @ORM\Column(type="string", length=20, nullable=true)
	 */
	protected $importance;

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
