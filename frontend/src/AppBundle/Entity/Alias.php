<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * Alias
 *
 * @ORM\Table(name="aliases")
 * @ORM\Entity
 */
class Alias
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
     * @ORM\Column(name="alias", type="string", length=64, precision=0, scale=0, nullable=false, unique=false)
     */
    private $alias;

    /**
     * @var string
     *
     * @ORM\Column(name="qid", type="string", length=16, precision=0, scale=0, nullable=false, unique=false)
     */
    private $qid;



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
