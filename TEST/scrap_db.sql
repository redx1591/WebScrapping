-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le :  mar. 23 oct. 2018 à 20:10
-- Version du serveur :  10.1.28-MariaDB
-- Version de PHP :  7.1.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `scrap_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `maroc`
--

CREATE TABLE `maroc` (
  `id` int(10) NOT NULL,
  `libProduit` varchar(191) NOT NULL,
  `slug` varchar(191) NOT NULL,
  `descProduit` longtext NOT NULL,
  `priceProduit` int(10) NOT NULL,
  `imgProduit` text NOT NULL,
  `numSeller` varchar(191) NOT NULL,
  `src` varchar(191) NOT NULL,
  `urlProduct` varchar(191) NOT NULL,
  `logo` varchar(191) NOT NULL,
  `origin` int(10) NOT NULL,
  `category` varchar(191) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `maroc`
--
ALTER TABLE `maroc`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `maroc`
--
ALTER TABLE `maroc`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
