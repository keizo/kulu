
 <?php if ($page == 0) { ?>
	 <div class="nodePreview<?php print ($sticky) ? " sticky" : ""; ?>">
	  <?php if ($title != ""): ?>
	  
	  <h2><div class="cornerR_yellow"></div>
	  
	  <a href="<?php print $node_url ?>" title="<?php print $title ?>">
	  <?php print $title ?></a>
	  </h2>
	  
	
	  <?php endif; ?>

	
	  <div class="content">
	  <div style="float:left"><?php print $taxonomy_images[0]; ?></div>
	  <?php print $content ?>
	  </div>
	  <?php if ($links): ?>

	  <div class="links"><?php print $links ?></div>
	  <?php endif; ?>
	</div>


  <?php } else { ?>
  
  
  <?php if ($title != ""): ?>
  <div id="title"><div class="cornerR_yellow"></div>
  <h1>
  <?php print $title ?>
  </h1>

  </div>

  <?php endif; ?>



  <div class="content"><div id="article_sidebar"></div>
  <p>
  <?php print $node->field_canoe_club_description[0]['view']; ?>
  </p>
  <h2>Links:</h2>
  <ul>
  <li>
  <?php 
    //validation code for link
	if ($node->field_canoe_club_website[0]['view']) {
		//$myurl = $node->flexinode_12;
    //	$myurl = check_url($myurl);
    //	$myurl = ERegI('^[a-z0-9_]+://', $myurl) ? $myurl : 'http://'.$myurl;  
	
		//print '<a href="' . $myurl . '">Official website for ' . $title . '</a>';
    print $node->field_canoe_club_website[0]['view'];
	} else print "No website available.";
  ?>
  </li>
  <li>
  <?php
  $mapcoords = $node->field_map_coordinates[0]['value'];
  if ($mapcoords) {
  $coords = explode(" ", check_plain($mapcoords));
  $coords = $coords[0] . "+" . $coords[1];
  print l("Map " . decode_entities($title),'http://maps.google.com/maps?q=' . $coords . '&ie=UTF8&z=15');
  } else print 'Map location not available.  ' . l('Add map coordinates.', 'node/' . $node->nid . '/edit');
  ?>
  </li>
  </ul>
  <br />
    <p><em><?php print $submitted; ?> </em></p>
  </div>


  <div class="links">See something wrong? <?php print l('Edit this page.', 'node/' . $node->nid . '/edit'); ?></div>
  <p><a href="/canoeclubs">Back to Canoe Club Directory</a></p>
  <?php } ?>

  
