const navigation = document.querySelector(".navigation");
const parser = new DOMParser();
let isNavigating = false;

function getFabToggleLink() {
    return document.querySelector(".navigation a[data-fab-toggle='true']");
}

function getFabMenu() {
    return document.querySelector(".navigation .fab-menu");
}

function closeFabMenu() {
    const menu = getFabMenu();
    const toggle = getFabToggleLink();
    if (!menu || !toggle) {
        return;
    }
    menu.classList.remove("open");
    menu.setAttribute("aria-hidden", "true");
    toggle.setAttribute("aria-expanded", "false");
    setActiveByPath(window.location.pathname);
    syncNavigationState();
}

function openFabMenu() {
    const menu = getFabMenu();
    const toggle = getFabToggleLink();
    if (!menu || !toggle) {
        return;
    }
    menu.classList.add("open");
    menu.setAttribute("aria-hidden", "false");
    toggle.setAttribute("aria-expanded", "true");

    const navItems = getNavItems();
    navItems.forEach((item) => item.classList.remove("active"));
    const toggleItem = toggle.closest(".list");
    if (toggleItem) {
        toggleItem.classList.add("active");
    }
    syncNavigationState(toggleItem || undefined);
}

function toggleFabMenu() {
    const menu = getFabMenu();
    if (!menu) {
        return;
    }
    if (menu.classList.contains("open")) {
        closeFabMenu();
    } else {
        openFabMenu();
    }
}

function buildFabMenu() {
    if (!navigation) {
        return;
    }

    if (getFabMenu()) {
        return;
    }

    const uploadHref = getFabToggleLink()?.getAttribute("href") || "/matriz/cargar/";
    const usersUploadHref = "/usuarios/";
    const sitesAmbiencesHref = "/sedes-ambientes/";
    const fichasHref = "/fichas/";
    const profileHref = document.querySelector(".navigation .list:nth-child(5) a")?.getAttribute("href") || "/perfil/";

    const menu = document.createElement("div");
    menu.className = "fab-menu";
    menu.setAttribute("aria-hidden", "true");
    menu.innerHTML = `
        <a class="fab-menu-btn fab-menu-btn--upload" data-fab-link="${uploadHref}" style="--tx:-108px; --ty:-30px; --delay:0ms;" title="Cargar matriz" aria-label="Cargar matriz" data-tooltip="cargar matriz">
            <span class="fab-menu-btn-inner"><img class="fab-menu-icon" src="/static/icons/add-square-svgrepo-com.svg" alt=""></span>
        </a>
        <a class="fab-menu-btn fab-menu-btn--users" data-fab-link="${usersUploadHref}" style="--tx:-82px; --ty:-78px; --delay:30ms;" title="Ver o cargar usuarios" aria-label="Ver o cargar usuarios" data-tooltip="ver o cargar usuarios"><span class="fab-menu-btn-inner"><img class="fab-menu-icon" src="/static/icons/user-plus-svgrepo-com.svg" alt=""></span></a>
        <a class="fab-menu-btn fab-menu-btn--sites" data-fab-link="${sitesAmbiencesHref}" style="--tx:-28px; --ty:-108px; --delay:60ms;" title="Sedes y ambientes" aria-label="Sedes y ambientes" data-tooltip="sedes y ambientes"><span class="fab-menu-btn-inner"><img class="fab-menu-icon" src="/static/icons/map-point-wave-svgrepo-com.svg" alt=""></span></a>
        <a class="fab-menu-btn" data-fab-link="${fichasHref}" style="--tx:28px; --ty:-108px; --delay:90ms;" title="Panel de fichas" aria-label="Panel de fichas" data-tooltip="panel de fichas"><span class="fab-menu-btn-inner"><img class="fab-menu-icon" src="/static/icons/archive-up-svgrepo-com.svg" alt=""></span></a>
        <a class="fab-menu-btn" data-fab-link="${profileHref}" style="--tx:82px; --ty:-78px; --delay:120ms;" title="Perfil" aria-label="Perfil"><span class="fab-menu-btn-inner">P</span></a>
        <a class="fab-menu-btn" data-fab-link="/matriz/" style="--tx:108px; --ty:-30px; --delay:150ms;" title="Ver matrices" aria-label="Ver matrices"><span class="fab-menu-btn-inner">V</span></a>
    `;

    navigation.appendChild(menu);
}

function bindFabMenuEvents() {
    if (!navigation) {
        return;
    }

    buildFabMenu();

    const menu = getFabMenu();
    const toggleLink = getFabToggleLink();
    if (!menu) {
        return;
    }

    if (toggleLink && !toggleLink.dataset.fabBound) {
        toggleLink.dataset.fabBound = "true";
        toggleLink.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            toggleFabMenu();
        });
    }

    menu.addEventListener("click", (event) => {
        const target = event.target.closest(".fab-menu-btn[data-fab-link]");
        if (!target) {
            return;
        }

        event.preventDefault();
        const href = target.getAttribute("data-fab-link");
        closeFabMenu();

        if (!href) {
            return;
        }

        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
            window.location.href = href;
            return;
        }

        loadPanel(href, true);
    });

    document.addEventListener("click", (event) => {
        const toggle = getFabToggleLink();
        const currentMenu = getFabMenu();
        if (!toggle || !currentMenu || !currentMenu.classList.contains("open")) {
            return;
        }

        const clickedToggle = event.target.closest("a[data-fab-toggle='true']");
        const clickedMenu = event.target.closest(".fab-menu");
        if (!clickedToggle && !clickedMenu) {
            closeFabMenu();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeFabMenu();
        }
    });
}

function stylesheetKey(hrefLike) {
    try {
        return new URL(hrefLike, window.location.origin).pathname;
    } catch {
        return null;
    }
}

function syncHeadStyles(nextDocument) {
    const currentLinks = Array.from(document.querySelectorAll("head link[rel='stylesheet']"));
    const nextLinks = Array.from(nextDocument.querySelectorAll("head link[rel='stylesheet']"));
    const currentByKey = new Map();

    currentLinks.forEach((link) => {
        const key = stylesheetKey(link.getAttribute("href") || link.href);
        if (key) {
            currentByKey.set(key, link);
        }
    });

    nextLinks.forEach((nextLink) => {
        const rawHref = nextLink.getAttribute("href");
        const key = stylesheetKey(rawHref || nextLink.href);
        if (!key) {
            return;
        }

        const resolvedHref = new URL(rawHref || nextLink.href, window.location.origin).toString();
        const existing = currentByKey.get(key);

        if (existing) {
            if (existing.href !== resolvedHref) {
                existing.href = resolvedHref;
            }
            currentByKey.delete(key);
            return;
        }

        const cloned = nextLink.cloneNode(true);
        cloned.setAttribute("data-spa-style", "true");
        cloned.href = resolvedHref;
        document.head.appendChild(cloned);
    });

    currentByKey.forEach((link) => {
        if (link.hasAttribute("data-spa-style")) {
            link.remove();
        }
    });
}

function getNavItems() {
    return Array.from(document.querySelectorAll(".navigation .list"));
}

function normalizePath(urlLike) {
    return new URL(urlLike, window.location.origin).pathname;
}

function setActiveByPath(pathname) {
    const navItems = getNavItems();
    if (navItems.length === 0) {
        return;
    }

    navItems.forEach((item) => item.classList.remove("active"));

    const targetItem = navItems.find((item) => {
        const link = item.querySelector("a[href]");
        if (!link) {
            return false;
        }
        const linkPath = normalizePath(link.getAttribute("href"));
        return (
            pathname === linkPath
            || (pathname.startsWith("/matriz/") && linkPath === "/matriz/cargar/")
            || (pathname.startsWith("/usuarios/") && linkPath === "/matriz/cargar/")
            || (pathname.startsWith("/sedes-ambientes/") && linkPath === "/matriz/cargar/")
            || (pathname.startsWith("/fichas/") && linkPath === "/matriz/cargar/")
        );
    });

    (targetItem || navItems[0]).classList.add("active");
}

function syncNavigationState(activeItem = document.querySelector(".navigation .list.active")) {
    const navItems = getNavItems();
    if (!navigation || navItems.length === 0) {
        return;
    }

    const activeIndex = Math.max(navItems.indexOf(activeItem), 0);
    navigation.style.setProperty("--items", navItems.length);
    navigation.style.setProperty("--active-index", activeIndex);
    navigation.classList.toggle("nav-edge-start", activeIndex === 0);
    navigation.classList.toggle("nav-edge-end", activeIndex === navItems.length - 1);
}

function executeContainerScripts(container) {
    if (!container) {
        return;
    }

    const scripts = Array.from(container.querySelectorAll("script"));
    scripts.forEach((oldScript) => {
        const newScript = document.createElement("script");

        Array.from(oldScript.attributes).forEach((attr) => {
            if (attr.name === "src") {
                const resolvedSrc = new URL(attr.value, window.location.origin).toString();
                newScript.setAttribute("src", resolvedSrc);
            } else {
                newScript.setAttribute(attr.name, attr.value);
            }
        });

        if (!oldScript.src) {
            newScript.textContent = oldScript.textContent;
        }

        oldScript.replaceWith(newScript);
    });
}

function initFlashMessages() {
    const messageList = document.querySelector(".message-list");
    const messageItems = Array.from(document.querySelectorAll(".message-list .message-item"));

    if (messageItems.length === 0) {
        return;
    }

    messageItems.forEach((item) => {
        if (item.dataset.autohideBound === "1") {
            return;
        }

        item.dataset.autohideBound = "1";
        window.setTimeout(() => {
            item.classList.add("is-hiding");
            item.addEventListener("animationend", () => {
                item.remove();
                if (messageList && messageList.children.length === 0) {
                    messageList.remove();
                }
            }, { once: true });
        }, 4000);
    });
}

async function loadPanel(url, pushStateEntry = true) {
    if (isNavigating) {
        return;
    }

    closeFabMenu();
    isNavigating = true;
    try {
        const response = await fetch(url, {
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        const html = await response.text();
        const doc = parser.parseFromString(html, "text/html");
        const nextMain = doc.querySelector("main.dashboard-shell");
        const nextNav = doc.querySelector(".navigation");

        if (!nextMain || !nextNav) {
            window.location.href = url;
            return;
        }

        const currentMain = document.querySelector("main.dashboard-shell");
        if (!currentMain) {
            window.location.href = url;
            return;
        }

        syncHeadStyles(doc);
        document.body.className = doc.body.className;
        currentMain.replaceWith(nextMain);
        executeContainerScripts(nextMain);
        initFlashMessages();

        const activePath = normalizePath(url);
        setActiveByPath(activePath);
        syncNavigationState();

        if (pushStateEntry && window.location.pathname !== activePath) {
            window.history.pushState({}, "", url);
        }

        if (doc.title) {
            document.title = doc.title;
        }
    } catch (error) {
        window.location.href = url;
    } finally {
        isNavigating = false;
    }
}

if (navigation) {
    bindFabMenuEvents();

    navigation.addEventListener("click", (event) => {
        // Guardado por compatibilidad: el listener directo del toggle ya gestiona este click.
        const toggle = event.target.closest("a[data-fab-toggle='true']");
        if (toggle) {
            event.preventDefault();
            toggleFabMenu();
            return;
        }

        const link = event.target.closest("a[data-spa='true']");
        if (!link) {
            return;
        }

        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
            return;
        }

        event.preventDefault();
        loadPanel(link.href, true);
    });

    window.addEventListener("popstate", () => {
        loadPanel(window.location.href, false);
    });
}

setActiveByPath(window.location.pathname);
syncNavigationState();
initFlashMessages();

/* ── Welcome Animation ── */
function playWelcomeAnimation() {
    const welcomeTag = document.querySelector('.welcome-tag');
    const senaLogo = document.querySelector('.sena-logo');

    if (!welcomeTag || !senaLogo) {
        return;
    }

    // Empujar logo hacia abajo y bajar el tag desde arriba
    senaLogo.classList.add('pushed-down');
    welcomeTag.classList.add('show');

    // A los 5 segundos, primero sube el tag y luego vuelve el logo.
    setTimeout(() => {
        welcomeTag.classList.remove('show');
        welcomeTag.classList.add('hide');

        welcomeTag.addEventListener('animationend', () => {
            welcomeTag.classList.remove('hide');
            senaLogo.classList.remove('pushed-down');
        }, { once: true });
    }, 5000);
}

// Ejecutar en cada carga/recarga de la página
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', playWelcomeAnimation);
} else {
    playWelcomeAnimation();
}
