(function () {
  "use strict";

  var config = window.OHMYGASRANGE_SITE;
  if (!config) return;

  var servicesById = config.services.reduce(function (acc, service) {
    acc[service.id] = service;
    return acc;
  }, {});

  var state = {
    activeFilter: "all",
    lastFocusedElement: null,
    currentPanelAlbumId: null,
    currentPanelServiceId: null
  };

  var $ = function (selector, parent) {
    return (parent || document).querySelector(selector);
  };

  var $$ = function (selector, parent) {
    return Array.prototype.slice.call((parent || document).querySelectorAll(selector));
  };

  function escapeHTML(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (char) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
      }[char];
    });
  }

  function isRealUrl(url) {
    return typeof url === "string" && url.trim() !== "" && url.trim() !== "#";
  }

  function getAlbum(albumId) {
    return config.albums.find(function (album) {
      return album.id === albumId;
    });
  }

  function serviceHasAnyLink(album, serviceId) {
    var hasAlbumLink = isRealUrl(album.albumLinks && album.albumLinks[serviceId]);
    var hasTrackLink = (album.tracks || []).some(function (track) {
      return isRealUrl(track.links && track.links[serviceId]);
    });
    return hasAlbumLink || hasTrackLink;
  }

  function getFirstLinkedService(album) {
    return config.services.find(function (service) {
      return serviceHasAnyLink(album, service.id);
    }) || config.services[0];
  }

  function getServiceLabel(serviceId) {
    return servicesById[serviceId] ? servicesById[serviceId].label : serviceId;
  }

  function getStatusClass(album) {
    return album.status === "upcoming" ? "upcoming" : "released";
  }

  function renderServiceStrip(album) {
    return config.services.map(function (service) {
      var isActive = serviceHasAnyLink(album, service.id);
      var title = isActive
        ? service.label + " 링크 열기"
        : service.label + " 링크 준비 중";

      return [
        '<button type="button" class="service-pill service-', escapeHTML(service.id), isActive ? '' : ' is-muted', '"',
        ' data-action="open-links" data-album-id="', escapeHTML(album.id), '" data-service-id="', escapeHTML(service.id), '"',
        ' aria-label="', escapeHTML(album.title + ' ' + title), '"',
        isActive ? '' : ' aria-disabled="true"',
        '>',
        '<span class="service-icon" aria-hidden="true">', escapeHTML(service.short), '</span>',
        '<span>', escapeHTML(service.label), '</span>',
        '</button>'
      ].join("");
    }).join("");
  }

  function renderTags(album) {
    return (album.tags || []).map(function (tag) {
      return '<span class="tag">' + escapeHTML(tag) + '</span>';
    }).join("");
  }

  function renderAlbumCard(album) {
    var statusClass = getStatusClass(album);
    return [
      '<article class="album-card reveal" data-album-card data-status="', escapeHTML(album.status), '" id="album-', escapeHTML(album.id), '">',
        '<div class="cover-zone">',
          '<span class="album-badge ', statusClass, '">', escapeHTML(album.statusLabel), '</span>',
          '<button type="button" class="cover-button" data-action="open-lightbox" data-img-src="', escapeHTML(album.cover), '" data-img-title="', escapeHTML(album.title + ' 앨범 커버'), '">',
            '<img src="', escapeHTML(album.cover), '" alt="', escapeHTML(album.title + ' 앨범 커버'), '" loading="lazy" width="3000" height="3000" />',
          '</button>',
        '</div>',
        '<div class="album-body">',
          '<div>',
            '<div class="album-kicker">',
              '<span class="pill">', escapeHTML(album.type), '</span>',
              '<span class="pill ', statusClass, '">', escapeHTML(album.releaseDate), '</span>',
              '<span class="pill">', escapeHTML(album.genre), '</span>',
              '<span class="pill">', escapeHTML(album.trackCount), '</span>',
            '</div>',
            '<h3 class="album-title">', escapeHTML(album.title), '<small>', escapeHTML(album.titleEn), '</small></h3>',
            '<p class="album-description">', escapeHTML(album.description), '</p>',
            '<div class="tag-row">', renderTags(album), '</div>',
          '</div>',
          '<div>',
            '<div class="album-actions">',
              '<button type="button" class="action-button primary" data-action="open-links" data-album-id="', escapeHTML(album.id), '" data-service-id="', escapeHTML(getFirstLinkedService(album).id), '">음악서비스 선택</button>',
              '<button type="button" class="action-button" data-action="open-lightbox" data-img-src="', escapeHTML(album.booklet), '" data-img-title="', escapeHTML(album.title + ' 앨범 소개 부클렛'), '">부클렛 보기</button>',
            '</div>',
            '<div class="service-strip" aria-label="', escapeHTML(album.title + ' 음악서비스'), '">',
              renderServiceStrip(album),
            '</div>',
          '</div>',
        '</div>',
      '</article>'
    ].join("");
  }

  function renderAlbums() {
    var grid = $("#album-grid");
    if (!grid) return;
    grid.innerHTML = config.albums.map(renderAlbumCard).join("");
    applyFilter(state.activeFilter);
  }

  function applyFilter(filter) {
    state.activeFilter = filter;
    $$('[data-album-card]').forEach(function (card) {
      var shouldShow = filter === "all" || card.getAttribute("data-status") === filter;
      card.classList.toggle("is-hidden", !shouldShow);
    });

    $$("[data-filter]").forEach(function (button) {
      var isActive = button.getAttribute("data-filter") === filter;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-selected", isActive ? "true" : "false");
    });
  }

  function renderServiceTabs(album, selectedServiceId) {
    return config.services.map(function (service) {
      var hasAlbumLink = isRealUrl(album.albumLinks && album.albumLinks[service.id]);
      var hasTrackLink = (album.tracks || []).some(function (track) {
        return isRealUrl(track.links && track.links[service.id]);
      });
      var hasAnyLink = hasAlbumLink || hasTrackLink;
      var isActive = service.id === selectedServiceId;

      return [
        '<button type="button" class="service-tab', isActive ? ' is-active' : '', hasAnyLink ? '' : ' is-empty', '"',
        ' data-action="select-service" data-service-id="', escapeHTML(service.id), '"',
        ' aria-label="', escapeHTML(service.label + (hasAnyLink ? ' 선택' : ' 링크 준비 중')), '">',
        escapeHTML(service.label),
        '</button>'
      ].join("");
    }).join("");
  }

  function renderAlbumLink(album, serviceId) {
    var serviceLabel = getServiceLabel(serviceId);
    var albumUrl = album.albumLinks && album.albumLinks[serviceId];

    if (isRealUrl(albumUrl)) {
      return [
        '<div class="link-row">',
          '<div>',
            '<strong>앨범 전체 듣기</strong><br />',
            '<span>', escapeHTML(serviceLabel), '에서 ', escapeHTML(album.title), ' 열기</span>',
          '</div>',
          '<a class="open-link" href="', escapeHTML(albumUrl), '" target="_blank" rel="noopener noreferrer">열기</a>',
        '</div>'
      ].join("");
    }

    if (album.status === "upcoming") {
      return '<div class="empty-state">이 앨범은 발매 예정입니다. 발매 후 <strong>assets/js/albums.js</strong>의 <strong>albumLinks</strong>에 URL을 넣으면 버튼이 자동 활성화됩니다.</div>';
    }

    return '<div class="empty-state">' + escapeHTML(serviceLabel) + ' 앨범 링크가 아직 입력되지 않았습니다. URL을 추가하면 즉시 활성화됩니다.</div>';
  }

  function renderTrackLinks(album, serviceId) {
    var serviceLabel = getServiceLabel(serviceId);
    var tracks = album.tracks || [];

    if (!tracks.length) {
      return '<div class="empty-state">곡별 링크 목록이 아직 없습니다. <strong>tracks</strong> 배열에 곡명과 서비스별 URL을 추가하면 이곳에 자동으로 표시됩니다.</div>';
    }

    var rows = tracks.map(function (track) {
      var url = track.links && track.links[serviceId];
      if (!isRealUrl(url)) return "";
      return [
        '<div class="link-row">',
          '<div>',
            '<strong>', escapeHTML(track.title), '</strong><br />',
            '<span>', escapeHTML(serviceLabel), ' 곡 링크</span>',
          '</div>',
          '<a class="open-link" href="', escapeHTML(url), '" target="_blank" rel="noopener noreferrer">열기</a>',
        '</div>'
      ].join("");
    }).filter(Boolean).join("");

    return rows || '<div class="empty-state">' + escapeHTML(serviceLabel) + ' 곡별 링크가 아직 입력되지 않았습니다.</div>';
  }

  function renderPanel(album, selectedServiceId) {
    var content = $("#panel-content");
    if (!content) return;

    content.innerHTML = [
      '<div class="panel-header">',
        '<img class="panel-cover" src="', escapeHTML(album.cover), '" alt="', escapeHTML(album.title + ' 커버'), '" width="3000" height="3000" />',
        '<div>',
          '<p class="eyebrow">', escapeHTML(album.type), ' · ', escapeHTML(album.statusLabel), '</p>',
          '<h2 id="panel-title">', escapeHTML(album.title), '</h2>',
          '<p>', escapeHTML(album.titleEn), ' · ', escapeHTML(album.releaseDate), '</p>',
        '</div>',
      '</div>',
      '<div class="service-tabs" role="tablist" aria-label="음악서비스 선택">',
        renderServiceTabs(album, selectedServiceId),
      '</div>',
      '<p class="panel-section-title">Album Link</p>',
      '<div class="link-stack">', renderAlbumLink(album, selectedServiceId), '</div>',
      '<p class="panel-section-title">Track Links</p>',
      '<div class="link-stack">', renderTrackLinks(album, selectedServiceId), '</div>'
    ].join("");
  }

  function openPanel(albumId, serviceId) {
    var album = getAlbum(albumId);
    if (!album) return;

    var selectedService = servicesById[serviceId] ? servicesById[serviceId] : getFirstLinkedService(album);
    var panel = $("#link-panel");
    var backdrop = $("#panel-backdrop");
    if (!panel || !backdrop) return;

    state.lastFocusedElement = document.activeElement;
    state.currentPanelAlbumId = albumId;
    state.currentPanelServiceId = selectedService.id;

    renderPanel(album, selectedService.id);
    backdrop.hidden = false;
    panel.hidden = false;
    document.body.classList.add("modal-open");

    var closeButton = $("[data-close-panel]", panel);
    if (closeButton) closeButton.focus({ preventScroll: true });
  }

  function closePanel() {
    var panel = $("#link-panel");
    var backdrop = $("#panel-backdrop");
    if (!panel || !backdrop) return;

    panel.hidden = true;
    backdrop.hidden = true;
    document.body.classList.remove("modal-open");
    state.currentPanelAlbumId = null;
    state.currentPanelServiceId = null;

    if (state.lastFocusedElement && typeof state.lastFocusedElement.focus === "function") {
      state.lastFocusedElement.focus({ preventScroll: true });
    }
  }

  function selectService(serviceId) {
    if (!state.currentPanelAlbumId) return;
    var album = getAlbum(state.currentPanelAlbumId);
    if (!album || !servicesById[serviceId]) return;
    state.currentPanelServiceId = serviceId;
    renderPanel(album, serviceId);
  }

  function openLightbox(src, title) {
    var lightbox = $("#lightbox");
    var image = $("#lightbox-image");
    var caption = $("#lightbox-title");
    if (!lightbox || !image || !caption) return;

    state.lastFocusedElement = document.activeElement;
    image.src = src;
    image.alt = title;
    caption.textContent = title;
    lightbox.hidden = false;
    document.body.classList.add("modal-open");

    var closeButton = $("[data-close-lightbox]", lightbox);
    if (closeButton) closeButton.focus({ preventScroll: true });
  }

  function closeLightbox() {
    var lightbox = $("#lightbox");
    var image = $("#lightbox-image");
    if (!lightbox || !image) return;

    lightbox.hidden = true;
    image.src = "";
    document.body.classList.remove("modal-open");

    if (state.lastFocusedElement && typeof state.lastFocusedElement.focus === "function") {
      state.lastFocusedElement.focus({ preventScroll: true });
    }
  }

  function setupEvents() {
    document.addEventListener("click", function (event) {
      var openLinksButton = event.target.closest('[data-action="open-links"]');
      if (openLinksButton) {
        openPanel(openLinksButton.getAttribute("data-album-id"), openLinksButton.getAttribute("data-service-id"));
        return;
      }

      var lightboxButton = event.target.closest('[data-action="open-lightbox"]');
      if (lightboxButton) {
        openLightbox(lightboxButton.getAttribute("data-img-src"), lightboxButton.getAttribute("data-img-title"));
        return;
      }

      var serviceTab = event.target.closest('[data-action="select-service"]');
      if (serviceTab) {
        selectService(serviceTab.getAttribute("data-service-id"));
        return;
      }

      if (event.target.closest("[data-close-panel]") || event.target.id === "panel-backdrop") {
        closePanel();
        return;
      }

      if (event.target.closest("[data-close-lightbox]") || event.target.id === "lightbox") {
        closeLightbox();
      }
    });

    $$("[data-filter]").forEach(function (button) {
      button.addEventListener("click", function () {
        applyFilter(button.getAttribute("data-filter"));
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closePanel();
        closeLightbox();
      }
    });

    window.addEventListener("scroll", function () {
      var header = $("[data-header]");
      if (!header) return;
      header.classList.toggle("is-scrolled", window.scrollY > 20);
    }, { passive: true });
  }

  function setupContact() {
    var email = config.contactEmail || "your-email@example.com";
    var mailLink = $("#contact-email");
    var year = $("#current-year");

    if (mailLink) {
      mailLink.textContent = email;
      mailLink.href = "mailto:" + encodeURIComponent(email).replace(/%40/g, "@");
    }

    if (year) {
      year.textContent = String(new Date().getFullYear());
    }
  }

  function setupReveal() {
    var elements = $$(".reveal");
    if (!elements.length) return;

    if (!("IntersectionObserver" in window)) {
      elements.forEach(function (element) {
        element.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    elements.forEach(function (element) {
      observer.observe(element);
    });
  }

  function setupTilt() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    document.addEventListener("pointermove", function (event) {
      var card = event.target.closest(".tilt-card, .album-card");
      if (!card || window.innerWidth < 900) return;

      var rect = card.getBoundingClientRect();
      var x = (event.clientX - rect.left) / rect.width;
      var y = (event.clientY - rect.top) / rect.height;
      var rotateY = (x - .5) * 7;
      var rotateX = (y - .5) * -7;

      card.style.setProperty("--rx", rotateX.toFixed(2) + "deg");
      card.style.setProperty("--ry", rotateY.toFixed(2) + "deg");
    });

    document.addEventListener("pointerout", function (event) {
      var card = event.target.closest(".tilt-card, .album-card");
      if (!card) return;
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    });
  }

  function setupCanvas() {
    var canvas = $("#visualizer");
    if (!canvas || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var ctx = canvas.getContext("2d");
    var width = 0;
    var height = 0;
    var particles = [];
    var rafId = null;

    function resize() {
      var ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = Math.floor(width * ratio);
      canvas.height = Math.floor(height * ratio);
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

      var count = Math.max(30, Math.min(90, Math.floor(width / 18)));
      particles = Array.from({ length: count }, function (_, index) {
        return {
          x: Math.random() * width,
          y: Math.random() * height,
          r: Math.random() * 2.6 + .8,
          speed: Math.random() * .35 + .08,
          phase: Math.random() * Math.PI * 2,
          hue: index % 3
        };
      });
    }

    function draw(time) {
      ctx.clearRect(0, 0, width, height);
      particles.forEach(function (p) {
        p.y -= p.speed;
        p.x += Math.sin(time * .001 + p.phase) * .18;
        if (p.y < -10) {
          p.y = height + 10;
          p.x = Math.random() * width;
        }

        var gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 7);
        if (p.hue === 0) {
          gradient.addColorStop(0, "rgba(255,79,216,.48)");
          gradient.addColorStop(1, "rgba(255,79,216,0)");
        } else if (p.hue === 1) {
          gradient.addColorStop(0, "rgba(53,242,255,.44)");
          gradient.addColorStop(1, "rgba(53,242,255,0)");
        } else {
          gradient.addColorStop(0, "rgba(255,181,69,.34)");
          gradient.addColorStop(1, "rgba(255,181,69,0)");
        }
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 7, 0, Math.PI * 2);
        ctx.fill();
      });
      rafId = window.requestAnimationFrame(draw);
    }

    resize();
    window.addEventListener("resize", resize, { passive: true });
    rafId = window.requestAnimationFrame(draw);

    window.addEventListener("pagehide", function () {
      if (rafId) window.cancelAnimationFrame(rafId);
    });
  }

  function init() {
    renderAlbums();
    setupContact();
    setupEvents();
    setupReveal();
    setupTilt();
    setupCanvas();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
