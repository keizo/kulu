<?php 
$my_rss_data = '<link rel="alternate" type="application/rss+xml" title="RSS - ' . $profile->profile_title . '" href="/blog/'. $profile->uid . '/feed" />';
drupal_set_html_head($my_rss_data);
global $user;
?>

<h1>
<?php if ($profile->profile_title) { 
    drupal_set_title($profile->profile_title);
    } else { $profile->profile_title = $profile->name . '\'s paddling profile'; } 
    print $profile->profile_title; 
?>

</h1>

<?php if($profile->profile_tagline) { print '<h3>' . $profile->profile_tagline . '</h3>'; } ?>

<?php if ($profile->uid == $user->uid): ?><p>(<em><a href="/node/add/blog" title="Write a blog entry!">Add a blog post</a></em>)</p>
    <?php endif ?>

<div id="sidebar_nospan">
    <?php  if($profile->picture) {print '<img src="/' . $profile->picture . '" />';}?>
<h2><?php print $profile->name ?></h2>
<?php if ($user->uid) { ?>
<h2>Personal</h2>
    <?php if($profile->profile_name): ?>
    <div class="fields">Name: <?php print check_plain($profile->profile_name) ?></div>
    <?php endif ?>
    <?php if($profile->profile_location): ?>
    <div class="fields">Location: <?php print check_plain($profile->profile_location) ?></div>
    <?php endif ?>
    <?php if($profile->profile_age): ?>
    <div class="fields">Age or division: <?php print check_plain($profile->profile_age) ?></div>
    <?php endif ?>
    <?php if($profile->profile_website): ?>
    <div class="fields">Website: <?php print l(check_plain($profile->profile_website),check_plain($profile->profile_website)) ?></div>
    <?php endif ?>
    <?php if($profile->profile_interests): ?>
    <div class="fields">Interests: <?php print check_plain($profile->profile_interests) ?></div>
    <?php endif ?>
    <?php if($profile->profile_about): ?>
    <div class="fields">More about me: <?php print check_plain($profile->profile_about) ?></div>
    <?php endif ?>
    
<h2>Paddling</h2>
    <?php if($profile->profile_clubs): ?>
    <div class="fields">Club(s): <?php print check_plain($profile->profile_clubs) ?></div>
    <?php endif ?>
    <?php if($profile->profile_started): ?>
    <div class="fields">Started: <?php print check_plain($profile->profile_started) ?></div>
    <?php endif ?>
    <?php if($profile->profile_paddlebag): ?>
    <div class="fields">In my paddle bag: <?php print check_plain($profile->profile_paddlebag) ?></div>
    <?php endif ?>
    <?php if($profile->profile_canoes): ?>
    <div class="fields">My canoe(s): <?php print check_plain($profile->profile_canoes) ?></div>
    <?php endif ?>
    <?php if($profile->profile_accomplishments): ?>
    <div class="fields">Accomplishments: <?php print check_plain($profile->profile_accomplishments) ?></div>
    <?php endif ?>
<?php } else { ?>
<p>You must login to view full profile.</p>
<?php } ?>
</div>

<div id="profile_blog">
    <!-- START - LATEST 10 BLOG ENTRIES -->
    <div class="profilefeeds">
    <?php $nlimit = 10; ?>
    <?php $userid=$profile->uid; ?>
    <?php $result1 = pager_query(db_rewrite_sql("SELECT n.nid, n.created FROM {node} n WHERE n.type = 'blog' AND n.status = 1 AND n.uid = $userid ORDER BY n.created DESC"), variable_get('default_nodes_main', $nlimit)); ?>
    <?php while ($node = db_fetch_object($result1)) {$output2 .= node_view(node_load(array('nid' => $node->nid)), 1);}; ?>
    
    <?php if($output2): ?>
    <?php print $output2; ?>
    <?php else: ?>
  <p><?php if ($profile->uid == $user->uid): ?>(<em><?php print $profile->name ?>, you can customize this page further by adding blog entries.</em>)
    <?php endif ?></p>
    <?php endif ?>
    </div>
    <!-- END - LATEST 10 BLOG ENTRIES -->
    <a href="/blog/<?php print $profile->uid ?>/feed" class="feed-icon"><img src="/misc/feed.png" alt="Syndicate content" title="Syndicate content" width="16" height="16" /></a>
</div>
