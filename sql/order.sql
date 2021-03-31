DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `rest_id` int NOT NULL,
  `table_no` int NOT NULL,
  `order_type` varchar(10) NOT NULL,
  `order_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comments` varchar(64),
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`)
);

DROP TABLE IF EXISTS `order_item`;
CREATE TABLE IF NOT EXISTS `order_item` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `qty` int NOT NULL,
  PRIMARY KEY (`order_id`,`item_id`)
);

DROP TABLE IF EXISTS `order_status`;
CREATE TABLE IF NOT EXISTS `order_status` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `status` int NOT NULL,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`)
);

INSERT INTO `order` (`rest_id`, `table_no`,`order_type`,`comments`) VALUES
(1, 30,'Dine-in', 'nil'),
(2, 4,'Dine-in', 'more chilli'),
(3, 55,'Take-away', 'nil'),
(4, 10,'Take-away', 'no lettuce');

INSERT INTO `order_item` (`order_id`, `item_id`,`qty`) VALUES
(1, 1,3),
(2, 2,2),
(3, 3,4),
(4, 4,6);

INSERT INTO `order_status` (`order_id`, `status`) VALUES
(1, 1),
(2, 2),
(3, 1),
(4, 1);


SELECT * FROM `order`;

SELECT * FROM `order_item`;

SELECT * FROM `order_status`; 
