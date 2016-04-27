<?php
namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table(name="communes")
 */

class Commune
{
	/**
	 * @ORM\Column(type="string", length=16)
	 * @ORM\Id
	 */
	protected $qid;

	/**
	 * @ORM\Column(type="string", length=64)
	 */
	protected $title;

	/**
	 * @ORM\Column(type="string", length=64)
	 */
	protected $wpTitle;

	/**
	 * @ORM\Column(type="string", length=64)
	 */
	protected $suggestStr;

	/**
	 * @ORM\Column(type="string", length=16)
	 */
	protected $insee;

	/**
	 * @ORM\Column(type="integer")
	 */
	protected $population;

	/**
	 * @ORM\Column(type="string", length=20)
	 */
	protected $badge;

	/**
	 * @ORM\Column(type="string", length=20)
	 */
	protected $progress;

	/**
	 * @ORM\Column(type="string", length=20)
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
	 * Set name
	 *
	 * @param string $name
	 *
	 * @return Commune
	 */
	public function setName($name)
	{
		$this->name = $name;

		return $this;
	}

	/**
	 * Get name
	 *
	 * @return string
	 */
	public function getName()
	{
		return $this->name;
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

	public static function computeSuggestStr($str)
	{
		$str = strtolower($str);
		$str = str_replace(
			array("-", "à", "â", "é", "è", "ê", "ï", "î", "ô", "ù", "û", "œ"), 
			array(" ", "a", "a", "e", "e", "e", "i", "i", "o", "u", "u", "oe"),
			$str
		);
		return $str;
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
}
