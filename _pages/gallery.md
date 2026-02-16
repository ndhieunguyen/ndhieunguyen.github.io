---
layout: page
title: gallery
permalink: /gallery/
description: A collection of events and memories.
nav: true
nav_order: 4
---

<div class="gallery">
  {% assign sorted_events = site.gallery | sort: "date" | reverse %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for event in sorted_events %}
      <div class="col mb-4">
        <a href="{{ event.url | relative_url }}">
          <div class="card h-100 hoverable">
            {% if event.img %}
              {%
                include figure.liquid
                loading="eager"
                path=event.img
                sizes = "250px"
                alt="event thumbnail"
                class="card-img-top"
              %}
            {% endif %}
            <div class="card-body">
              <h2 class="card-title">{{ event.title }}</h2>
              <p class="post-meta">{{ event.date | date: "%B %-d, %Y" }}</p>
              <p class="card-text">{{ event.description }}</p>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>
</div>
