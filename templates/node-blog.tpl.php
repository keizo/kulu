
 <?php if ($page == 0) { ?>
	 <div class="">
	  <?php if ($title != ""): ?>
	  
	  <h2>
	  
	  <a href="<?php print $node_url ?>" title="<?php print $title ?>">
	  <?php print $title ?></a>
	  </h2>
	  
	
	  <?php endif; ?>

	
	  <div class="content">
	  
	  <?php 
	  if (isset($taxonomy_images)) {
	  ?><div style="float:left"> <?php
	  foreach ($taxonomy_images as $taxonomy_image) {
	  print $taxonomy_image; 
	  ?></div><?php
	  } }
	  ?>
	  
	  <?php print $content ?>
	  </div>
	  <?php if ($links): ?>

	  <div class="links"><?php print $links ?></div>
	  <?php endif; ?>
	</div>

  <?php } else { ?>
  <?php if ($title != ""): ?>
  <div id="">
  <h1>
  <?php print $title ?>
  </h1>
  <div id="info"><?php print $submitted .'<span class="taxonomy">'. ($submitted ? ' :: ' : '') . $terms .'</span>' ?></div>
  </div>

  <?php endif; ?>



  <div class="content">
  <?php print $content ?>
  </div>
  <?php if ($links): ?>

  <div class="links"><strong><?php print $links ?></strong></div>
  <?php endif; ?>
  <?php } ?>

  
