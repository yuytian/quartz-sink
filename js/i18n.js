/**
 * MOOSUN i18n Engine
 * Loads language JSON files from /i18n/ directory dynamically.
 * Falls back to embedded default (zh-CN) for file:// protocol.
 * Supports: zh-CN, en, zh-TW, ms, ar (Arabic RTL)
 */
(function () {
  'use strict';

  const I18N = {
    // Current language
    current: 'zh-CN',
    // Cache of loaded translations
    _cache: {},

    /**
     * Load a language JSON file via fetch.
     * Returns the parsed JSON object, or null on failure.
     */
    async _fetch(lang) {
      try {
        const resp = await fetch(`i18n/${lang}.json`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        this._cache[lang] = data;
        return data;
      } catch (e) {
        console.warn(`i18n: Could not load i18n/${lang}.json — ${e.message}`);
        return null;
      }
    },

    /**
     * Get translation dictionary for a language.
     * Uses cache, fetch, or fallback chain.
     */
    async _load(lang) {
      // 1. Already cached?
      if (this._cache[lang]) return this._cache[lang];

      // 2. Try to fetch from server
      const data = await this._fetch(lang);
      if (data) return data;

      // 3. Fallback to zh-CN (always embedded as default)
      if (lang !== 'zh-CN') {
        return this._load('zh-CN');
      }

      // 4. Ultimate fallback — empty dict (should never reach here)
      return {};
    },

    /**
     * Get a single translation string by key.
     */
    t(key) {
      const dict = this._cache[this.current] || this._cache['zh-CN'] || {};
      return dict[key] || key;
    },

    /**
     * Walk DOM and apply all data-i18n and data-i18n-attr translations.
     */
    applyToDOM() {
      // Text content
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (key) el.textContent = this.t(key);
      });

      // Attributes (aria-label, title, placeholder, content, etc.)
      document.querySelectorAll('[data-i18n-attr]').forEach(el => {
        const attrStr = el.getAttribute('data-i18n-attr');
        if (!attrStr) return;
        // Format: "attr:key" or "attr:key;attr2:key2"
        attrStr.split(';').forEach(pair => {
          const [attr, key] = pair.split(':').map(s => s.trim());
          if (attr && key) el.setAttribute(attr, this.t(key));
        });
      });

      // Meta description
      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) metaDesc.setAttribute('content', this.t('meta.desc'));

      // Document title
      document.title = this.t('meta.title');

      // HTML lang attribute
      document.documentElement.lang = this.current;
    },

    /**
     * Set page direction (LTR / RTL for Arabic).
     */
    setDirection() {
      const isRTL = this.current === 'ar';
      document.documentElement.dir = isRTL ? 'rtl' : 'ltr';

      // Update font variables for Arabic script
      if (isRTL) {
        document.documentElement.style.setProperty(
          '--font-heading',
          "'Noto Sans Arabic', 'Noto Sans SC', 'Inter', system-ui, sans-serif"
        );
        document.documentElement.style.setProperty(
          '--font-body',
          "'Noto Sans Arabic', 'Noto Sans SC', 'Inter', system-ui, sans-serif"
        );
        this._loadArabicFont();
      }
    },

    /**
     * Dynamically load Arabic font when switching to ar.
     */
    _loadArabicFont() {
      if (document.querySelector('link[data-font="arabic"]')) return; // already loaded
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.setAttribute('data-font', 'arabic');
      link.href = 'https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap';
      document.head.appendChild(link);
    },

    /**
     * Save language preference to localStorage.
     */
    persist(lang) {
      try {
        localStorage.setItem('moosun-lang', lang);
      } catch (e) { /* not available */ }
    },

    /**
     * Detect initial language.
     * Priority: URL param → localStorage → browser → default zh-CN
     */
    detect() {
      // 1. URL query ?lang=xx
      const urlParams = new URLSearchParams(window.location.search);
      const urlLang = urlParams.get('lang');
      if (urlLang && this._isSupported(urlLang)) return urlLang;

      // 2. localStorage
      try {
        const stored = localStorage.getItem('moosun-lang');
        if (stored && this._isSupported(stored)) return stored;
      } catch (e) { /* not available */ }

      // 3. Browser preference
      const browserLang = navigator.language || navigator.userLanguage;
      if (browserLang) {
        if (this._isSupported(browserLang)) return browserLang;
        const prefix = browserLang.split('-')[0];
        const match = this._supported().find(k => k.startsWith(prefix));
        if (match) return match;
      }

      // 4. Default
      return 'zh-CN';
    },

    _supported() {
      return ['zh-CN', 'en', 'zh-TW', 'ms', 'ar'];
    },

    _isSupported(lang) {
      return this._supported().includes(lang);
    },

    /**
     * Switch to a new language.
     */
    async setLang(lang) {
      if (!this._isSupported(lang)) return;
      if (lang === this.current) return;

      const data = await this._load(lang);
      if (!data) return;

      this.current = lang;
      this._cache[lang] = data;
      this.setDirection();
      this.applyToDOM();
      this.persist(lang);
      this._updateSwitchers(lang);
    },

    /**
     * Sync both desktop and mobile language select dropdowns.
     */
    _updateSwitchers(lang) {
      [document.getElementById('langSwitcher'), document.getElementById('langSwitcherMobile')]
        .filter(Boolean)
        .forEach(select => { select.value = lang; });
    },

    /**
     * Initialize: detect language, load translations, apply to page.
     */
    async init() {
      const detected = this.detect();
      const data = await this._load(detected);
      if (!data) {
        console.error('i18n: Failed to load any translations.');
        return;
      }

      this.current = detected;
      this._cache[detected] = data;
      // Always warm zh-CN cache as fallback
      if (detected !== 'zh-CN') {
        this._fetch('zh-CN').then(d => { if (d) this._cache['zh-CN'] = d; });
      }

      this.setDirection();
      this.applyToDOM();
      this._updateSwitchers(detected);
    },
  };

  // Expose
  window.I18N = I18N;

  // Auto-init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => I18N.init());
  } else {
    I18N.init();
  }
})();
