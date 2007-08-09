<?php //$Id: node-og.tpl.php,v 1.1.2.3 2005/05/31 11:24:49 weitzman Exp $ 
?>
<div class="node<?php print ($sticky) ? " sticky" : ""; ?>">
  <?php if ($page == 0): ?>
    <h2><a href="<?php print $node_url ?>" title="<?php print $title ?>"><?php print $title ?></a></h2>
  <?php endif; ?>
<?php //$node = phptemplate_og_view(); 
//print var_dump($node);?>

  <div class="content">
    <?php print $content ?>
  </div>

</div>
