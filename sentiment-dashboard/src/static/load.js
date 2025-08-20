function load_script(url) {
  const script = document.createElement('script');
  script.src = url;
  script.async = true;
  script.type = "module";
  document.head.appendChild(script);
}

function load_component(name) {
  load_script(`/static/components/${name}/${name}.js`)
}

load_component("navbar")
load_component("button")
