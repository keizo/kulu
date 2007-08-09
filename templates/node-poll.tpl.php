<?php 
drupal_set_html_head('<style type="text/css" media="all">@import "/' . path_to_theme() . '/node-poll.css";</style>');  
?> 

 <?php if ($page == 0) { ?>
	 <div class="nodePreview<?php print ($sticky) ? " sticky" : ""; ?>">
	  <?php if ($title != ""): ?>
	  
	  <h2><div class="cornerR_yellow"></div>
	  
	  <a href="<?php print $node_url ?>" title="<?php print $title ?>">
	  <?php print $title ?></a>
	  </h2>
	  
	
	  <?php endif; ?>

	
	  <div class="content">
	  
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

  
