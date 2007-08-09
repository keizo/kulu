
 <?php if ($page == 0) { ?>
	 <div class="teaser<?php print ($sticky) ? " sticky" : ""; ?>">
	  <?php if ($title != ""): ?>
	  <div style="float:right">
	  <?php 
	  if (isset($taxonomy_images)) {
	  foreach ($taxonomy_images as $taxonomy_image) {
	  print $taxonomy_image; 
	  } }
	  ?></div>
	  <h2>	  
	  <a <?php print $node->readmore ? 'href="'.$node_url.'" ' : 'class="nolink" '; ?>title="<?php print 'posted ' . format_date($node->created) ?>">
	  <?php print $title ?></a>
	  </h2>
	
	  <?php endif; ?>

	
	  <div class="content">

	  
	  <?php print $content ?>
	  </div>
	  <?php if ($links): ?>

	  <div class="links"><span class="terms">Filed in <?php print $terms ?></span>
	  <?php print '<a href="' . $node_url . '#comment">comments (' . $node->comment_count . ')</a>'; 
	  print ' | <a href="' . $node_url . '" title="permanent link">#</a>';?>
	  </div>
	  <?php endif; ?>
	</div>

  <?php } else { ?>
  <div id="story">
  <?php if ($title != ""): ?>
    	  <div class="taxonomy-image">
	  <?php 
	  if (isset($taxonomy_images)) {
	  foreach ($taxonomy_images as $taxonomy_image) {
	  print $taxonomy_image; 
	  } }
	  ?></div>
  <div id="title">
  <h1>
  <?php print $title ?>
  </h1>
  <div id="info" class="small"><?php //print var_dump($node) ?>
    <?php print '<span class="taxonomy">Filed in ' . $terms .'</span>' ?></div>
  </div>

  <?php endif; ?>



  <div class="content">

  <!--<div id="article_sidebar"><h3 class="title">Related Info</h3>
  <?php 
  	if (isset($taxonomy_text)) {
	foreach ($taxonomy_text as $taxonomy_texxt) {
	  print $taxonomy_texxt; 
	} } ?>
  </div> -->
  <?php print $content ?>
  
  <?php print '<p><em>Posted by ' . l($node->name,'user/'.$node->uid) . ' on ' . format_date($node->created) . '</em></p>'; ?>
  </div>
  <?php if ($links): ?>

  <div class="links"><strong><?php print $links ?></strong>
  <?php print ' | <a href="' . $node_url . '" title="permanent link">#</a>'; ?>
  </div>
  <?php endif; ?>
  </div>
  <?php } ?>

  
