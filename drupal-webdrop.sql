ALTER TABLE  `url_alias` DROP  `pid`;

ALTER TABLE  `users` CHANGE  `pass`  `password` VARCHAR( 32 ) NOT NULL;
    
ALTER TABLE  `users` CHANGE  `mail`  `email` VARCHAR( 64 );
    
ALTER TABLE  `permission` DROP  `tid`;

ALTER TABLE  `users` DROP INDEX  `name` ,
ADD INDEX  `name` (  `name` );
    
ALTER TABLE  `users` ADD INDEX (  `email` );
    
ALTER TABLE  `users` ADD  `remember_me` TINYINT( 1 ) DEFAULT  '0' NOT NULL ;
    
###################### do this for all tables that use sequences
ALTER TABLE users AUTO_INCREMENT = value;



-- 
-- Table structure for table `cache_node`
-- 

CREATE TABLE `cache_node` (
  `nid` int(10) unsigned NOT NULL default '0',
  `vid` int(10) unsigned NOT NULL default '0',
  `cache` longtext,
  `created` int(11) NOT NULL default '0',
  `expire` int(11) NOT NULL default '0',
  PRIMARY KEY  (`nid`,`vid`),
  KEY `expire` (`expire`)
) TYPE=MyISAM;


ALTER TABLE  `node_revisions` DROP PRIMARY KEY ,
ADD PRIMARY KEY (  `nid` ,  `vid` )
    
ALTER TABLE  `node` DROP INDEX  `vid`