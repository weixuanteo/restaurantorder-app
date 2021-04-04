<<<<<<< Updated upstream
DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant` (
  `rest_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_open` boolean NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`rest_id`)
);

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `price` float NOT NULL,
  `description` varchar(400) NOT NULL,
  `category` varchar(100) NOT NULL,
  `img_url` varchar(100) NOT NULL,
  PRIMARY KEY (`item_id`)
);

DROP TABLE IF EXISTS `restaurant_items`;
CREATE TABLE IF NOT EXISTS `restaurant_items` (
  `rest_id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  PRIMARY KEY (`rest_id`,`item_id`)
);

INSERT INTO `restaurant` (`rest_id`, `name`,`is_open`,`address`) VALUES
(1, 'Niku Katsumata',true, 'Duxton, Tanjong Pagar'),
(2, 'Carrotsticks and Cravings (Dempsey)',true, 'Central, Dempsey, Tanglin'),
(3, 'Tsuta Japanese Soba Noodles (Funan)',true, 'City Hall');

INSERT INTO `item` (`item_id`, `name`,`price`,`description`,`category`,`img_url`) VALUES
(1, 'Ajitama Teriyaki Chicken Spicy Soba',17.80,'Looking for a little kick of spices? This dish features tender teriyaki chicken alongside a flavoured egg, mushrooms, onions, vegetables and hot sauce with tomato paste served on the side for you to add to your liking!','noodel','assets/img/food2.jpg'),
(2, 'Wagyu Tartare',22,'This signature dish is a crowd-favourite as it delivers unique flavours and tantalises your palate with its freshness.','beef','assets/img/food2.jpg'),
(3, 'A4 Wagyu Donburi with Bonito Broth',25,'This donburi is not just any meat on rice - it consists of thin slices of perfectly-seared wagyu full of juiciness and flavour.','beef','assets/img/food2.jpg');

INSERT INTO `restaurant_items` (`rest_id`, `item_id`) VALUES
(1, 1),
(1, 2),
(3, 1),
(2, 1);


select*from `restaurant`;
select*from `item`;
select*from `restaurant_items`;
=======
use `restaurant`;
DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant` (
  `rest_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `is_open` boolean NOT NULL,
  `address` varchar(128) NOT NULL,
  PRIMARY KEY (`rest_id`)
);

INSERT INTO `restaurant` (`name`, `is_open`,`address`) VALUES
('rest 1', 1,"sengkang"),
('rest 2', 0,"hougang"),
('rest 3', 0,"punggol"),
('rest 4', 1,"orchard");
>>>>>>> Stashed changes
