import { c as createComponent, d as createAstro, m as maybeRenderHead, u as unescapeHTML, a as renderTemplate, n as createVNode, F as Fragment, _ as __astro_tag_component__ } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import 'clsx';
import { a as $$ToggleTheme } from './ToggleTheme_FEZIKbSa.mjs';

const $$Astro = createAstro("https://mofa.ai");
const $$DListItem = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$DListItem;
  const { dt } = Astro2.props;
  const content = await Astro2.slots.render("default");
  return renderTemplate`${maybeRenderHead()}<h6>${unescapeHTML(dt)}</h6> <div class="dd ml-8">${unescapeHTML(content)}</div>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/ui/DListItem.astro", void 0);

const frontmatter = {
  "publishDate": "2023-07-17T00:00:00.000Z",
  "title": "AstroWind template in depth",
  "excerpt": "While easy to get started, Astrowind is quite complex internally.  This page provides documentation on some of the more intricate parts.",
  "image": "https://images.unsplash.com/photo-1534307671554-9a6d81f4d629?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1651&q=80",
  "category": "Documentation",
  "tags": ["astro", "tailwind css", "front-end"],
  "metadata": {
    "canonical": "https://astrowind.vercel.app/astrowind-template-in-depth"
  },
  "readingTime": 5
};
function getHeadings() {
  return [{
    "depth": 2,
    "slug": "overview",
    "text": "Overview"
  }, {
    "depth": 2,
    "slug": "styling",
    "text": "Styling"
  }, {
    "depth": 3,
    "slug": "dark-mode",
    "text": "Dark Mode"
  }, {
    "depth": 2,
    "slug": "advanced-slot-usage",
    "text": "Advanced Slot Usage"
  }, {
    "depth": 3,
    "slug": "alternate-usage",
    "text": "Alternate usage"
  }, {
    "depth": 3,
    "slug": "yet-another-step",
    "text": "Yet Another Step"
  }];
}
function _createMdxContent(props) {
  const _components = {
    blockquote: "blockquote",
    code: "code",
    em: "em",
    h2: "h2",
    h3: "h3",
    li: "li",
    ol: "ol",
    p: "p",
    pre: "pre",
    span: "span",
    ...props.components
  };
  return createVNode(Fragment, {
    children: [createVNode(_components.h2, {
      id: "overview",
      children: "Overview"
    }), "\n", createVNode(_components.p, {
      children: ["It can be a somewhat daunting task trying to get a handle on ", createVNode(_components.em, {
        children: "AstroWind"
      }), " internals, and particularly various points of usage."]
    }), "\n", createVNode(_components.p, {
      children: ["This page outlines and clarifies some of the techniques found in ", createVNode(_components.em, {
        children: "AstroWind"
      }), ". Use it as a guide for further modification, or an instructional for techniques to use in your own endeavors."]
    }), "\n", createVNode(_components.h2, {
      id: "styling",
      children: "Styling"
    }), "\n", createVNode(_components.p, {
      children: ["As the name suggests, ", createVNode(_components.em, {
        children: "AstroWind"
      }), " relies on ", createVNode(_components.em, {
        children: "TailWind"
      }), " for styling. Furthermore, ", createVNode(_components.em, {
        children: "AstroWind"
      }), " defines custom low level style settings which are incorporated into ", createVNode(_components.em, {
        children: "TailWind"
      }), " seamlessly, and which provides consistency for higher level styling constructs, as well as enabling dark mode."]
    }), "\n", createVNode(_components.p, {
      children: ["The styling mechanism consists of the following files (all paths are prefixed with ", createVNode(_components.code, {
        children: "/src/"
      }), " ):"]
    }), "\n", createVNode($$DListItem, {
      dt: "assets/styles/tailwind.css",
      children: createVNode(_components.p, {
        children: ["This file is essentially an extension of ", createVNode(_components.em, {
          children: "TailWind’s"
        }), " base.css. High-level component styles are defined here. Note\nalso styling on elements selected by ‘attribute’ selectors at the bottom of the files, particularly those selected by\n‘data’ attributes."]
      })
    }), "\n", createVNode($$DListItem, {
      dt: "components/CustomStyles.astro",
      children: createVNode(_components.p, {
        children: "Defines custom colors and fonts. For these to take effect in the ‘base.css’ file, they need to be loaded in the html\nheader section. See next."
      })
    }), "\n", createVNode($$DListItem, {
      dt: "layouts/Layout.astro",
      children: createVNode(_components.p, {
        children: ["This layout is used for all of the pages rendered by ", createVNode(_components.em, {
          children: "AstroWind"
        }), ". The contents of ", createVNode(_components.em, {
          children: "tailwind.css"
        }), " and\n", createVNode(_components.em, {
          children: "CustomStyles.astro"
        }), " component, described above, is injected into the html header."]
      })
    }), "\n", createVNode(_components.h3, {
      id: "dark-mode",
      children: "Dark Mode"
    }), "\n", createVNode(_components.p, {
      children: [createVNode(_components.em, {
        children: "Dark Mode"
      }), " is triggered by the little ‘sunlight’ icon:", createVNode($$ToggleTheme, {}), "in the page header. It is defined in the ", createVNode(_components.em, {
        children: "components/common/ToggleTheme.astro"
      }), ", but the event is attached and the action defined in ", createVNode(_components.em, {
        children: "components/common/BasicScripts.astro"
      }), " in the following snippet:"]
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "javascript",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "attachEvent"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "("
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "'[data-aw-toggle-color-scheme]'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ", "
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "'click'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ", "
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "function"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " () {"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "  if"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " (defaultTheme."
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "endsWith"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "("
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "':only'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ")) {"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "    return"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ";"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  }"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  document.documentElement.classList."
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "toggle"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "("
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "'dark'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ");"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  localStorage.theme "
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " document.documentElement.classList."
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "contains"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "("
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "'dark'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ") "
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "?"
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: " 'dark'"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " :"
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: " 'light'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ";"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "});"
          })
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: ["Note that this is a client event. ", createVNode(_components.em, {
        children: "BasicScripts.astro"
      }), " defines several other client-side functionality as well as this one."]
    }), "\n", createVNode(_components.h2, {
      id: "advanced-slot-usage",
      children: "Advanced Slot Usage"
    }), "\n", createVNode(_components.p, {
      children: [createVNode(_components.em, {
        children: "slots"
      }), " are part of the component implementation, which is a common concept among many frameworks, including ", createVNode(_components.em, {
        children: "Astrojs"
      }), ". The typical slot definition in a component looks like this:"]
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "astro",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "---"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "// (file: MyComponent.astro)"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "const"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " { "
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "title"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " } "
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " Astro.props;"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "export"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " interface"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " Props"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " {"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#FFAB70"
            },
            children: "  title"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: ":"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: " string"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ";"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "}"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "---"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "<"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "h2"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">{title}</h2>"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "slot"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " />"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "  <!-- slot contents injected here -->"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "></"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "</"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: "And in usage elsewhere:"
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "astro",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "import MyComponent from \"~/components/MyComponent\"; ..."
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "<"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "MyComponent"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " someArg"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"A Slot example\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "p"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">This content will be displayed in the slot</"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "p"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "</"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "MyComponent"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        })]
      })
    }), "\n", createVNode(_components.h3, {
      id: "alternate-usage",
      children: "Alternate usage"
    }), "\n", createVNode(_components.p, {
      children: "There’s another way we can use slots, useful particularly when a component can have markdown content is as follows (study carefully…):"
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "astro",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "---"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "// (file: MyComponent.astro)"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "const"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " { "
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "title"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " } "
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " Astro.props;"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "export"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " interface"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " Props"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " {"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#FFAB70"
            },
            children: "  title"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: ":"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: " string"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ";"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "}"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "const"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: " content"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: ":"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: " string"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " ="
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " await"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " Astro.props."
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "render"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "("
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "'default'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ");"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "---"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "// renders the html to the 'content' variable"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "<"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "h2"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">{title}</h2>"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " set:html"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "{content}"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " />"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "  <!-- slot contents injected here -->"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "></"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "</"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "div"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: "Whoa!! What’s going on here?"
    }), "\n", createVNode(_components.p, {
      children: ["Notice there is no slot definition in the html portion of the component. Instead, what we do is have ", createVNode(_components.em, {
        children: "Astro"
      }), " render the slot content (here, the ‘default’ content, but you can also render named slots) into a variable, and then use that content in a ", createVNode(_components.em, {
        children: "div"
      }), " (for instance)."]
    }), "\n", createVNode(_components.p, {
      children: "So, if the usage is in a markdown file, like so:"
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "mdx",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "import MyComponent from '../../components/MyComponent';"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#79B8FF",
              fontWeight: "bold"
            },
            children: "# Using the above component in a .mdx file (that can take components)"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "{' '}"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "<MyComponent title=\"This is a slot implementor\">### Here is some markdown content - With a bullet item.</MyComponent>"
          })
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: [createVNode(_components.em, {
        children: "MyComponent"
      }), " renders the markdown to html and then injects it into the div."]
    }), "\n", createVNode(_components.p, {
      children: ["This actually has a big advantage — consider that with the normal usage you don’t have access to the slot contents: ", createVNode(_components.em, {
        children: "Astro"
      }), " just plops the content into the ", createVNode(_components.em, {
        children: "<slot/>"
      }), " tag. Using this method, however, allows you to access the content and further manipulate it before it gets inserted into the html."]
    }), "\n", createVNode(_components.p, {
      children: "This allows a great deal of flexibility in component design."
    }), "\n", createVNode(_components.h3, {
      id: "yet-another-step",
      children: "Yet Another Step"
    }), "\n", createVNode(_components.p, {
      children: ["Now, we get to the techniques used in ", createVNode(_components.em, {
        children: "AstroWind"
      }), ", we’ll use the ", createVNode(_components.em, {
        children: "pages/index.astro"
      }), " file to illustrate."]
    }), "\n", createVNode(_components.p, {
      children: ["You’ll note that the index file imports a lot of components, each one roughly analagous to a panel in the index page. Each of these components, in turn, is instantiated sequentially throughout the page. But, you’ll notice that some of them use this kind of construct (we’ll use the last section, ", createVNode(_components.em, {
        children: "CallToAction"
      }), ", as it is most illustrative of the technique):"]
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "astro",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "<"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "CallToAction"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "  callToAction"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "{{"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "    text:"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " '"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "Get"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " template"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "',"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "    href:"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " '"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "https:"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "//"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "github.com"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "/"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "onwidget"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "/"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "astrowind"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "',"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "    icon:"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " '"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "tabler:download"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "',"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  }}"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "Fragment"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " slot"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"title\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "    Astro + <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "br"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " class"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"block sm:hidden\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " /><"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "span"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " class"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"sm:whitespace-nowrap\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">Tailwind CSS</"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "span"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  </"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "Fragment"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  <"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "Fragment"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " slot"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"subtitle\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "    Be very surprised by these huge fake numbers you are seeing on this page. <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "br"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " class"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"hidden md:inline\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " />Don't waste"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "    more time! :P"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  </"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "Fragment"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "</"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "CallToAction"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: "Some things to note, here:"
    }), "\n", createVNode($$DListItem, {
      dt: "The <em>callToAction</em> argument",
      children: createVNode(_components.p, {
        children: "This argument is actually being passed a javascript object — not a string. (However, in the TS definition, it could\nbe a string…)"
      })
    }), "\n", createVNode($$DListItem, {
      dt: "There are several <em>Fragment</em> children",
      children: createVNode(_components.p, {
        children: ["Furthermore, these <Fragment/> elements each have a ", createVNode(_components.em, {
          children: "slot=“(value)”"
        }), " specifier."]
      })
    }), "\n", createVNode(_components.p, {
      children: ["The latter seems odd, because <Fragment/> is a built-in component over which you have no control, and doesn’t have a provision for rendering slots, ", createVNode("em", {
        children: "per se"
      }), "."]
    }), "\n", createVNode(_components.p, {
      children: ["The answer lies in a paragraph in the ", createVNode(_components.em, {
        children: "Astro"
      }), " docs, slots section, which states:"]
    }), "\n", createVNode(_components.blockquote, {
      children: ["\n", createVNode(_components.p, {
        children: ["Use a ", createVNode(_components.code, {
          children: "slot=\"my-slot\""
        }), " attribute on the child element that you want to pass through to a matching slot ", createVNode(_components.code, {
          children: "name=\"my-slot\" />"
        }), " placeholder in your component."]
      }), "\n"]
    }), "\n", createVNode(_components.p, {
      children: "That’s pretty concise and a bit of a head-scratcher to read, but basically what it says is that:"
    }), "\n", createVNode(_components.ol, {
      children: ["\n", createVNode(_components.li, {
        children: "Given a component that defines a slot:"
      }), "\n", createVNode(_components.li, {
        children: "you can reference a slot from a child element of that component and,"
      }), "\n", createVNode(_components.li, {
        children: ["provide content to the parent component’s slot from the child by naming the slot in the child with a ", createVNode(_components.code, {
          children: "slot=\"<slot-name>\""
        }), " property assignment, where the ", createVNode(_components.em, {
          children: "slot-name"
        }), " is the parent’s slot."]
      }), "\n"]
    }), "\n", createVNode(_components.p, {
      children: ["So, in the example above, the ", createVNode(_components.em, {
        children: "CallToAction"
      }), " component defines the ", createVNode(_components.em, {
        children: "subtitle"
      }), " slot, and the following ", createVNode(_components.em, {
        children: "<Fragment slot=“subtitle”>"
      }), " populates the slot with the following content:"]
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "astro",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "<"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "Fragment"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " slot"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"subtitle\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  Be very surprised by these huge fake numbers you are seeing on this page. <"
          }), createVNode(_components.span, {
            style: {
              color: "#85E89D"
            },
            children: "br"
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: " class"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "\"hidden md:inline\""
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " />Don't waste"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "  more time! :P"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "</"
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "Fragment"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ">"
          })]
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: ["And, the ", createVNode(_components.em, {
        children: "CallToAction"
      }), " component defines and renders it thusly:"]
    }), "\n", createVNode(_components.pre, {
      class: "astro-code github-dark",
      style: {
        backgroundColor: "#24292e",
        color: "#e1e4e8",
        overflowX: "auto"
      },
      tabindex: "0",
      "data-language": "astro",
      children: createVNode(_components.code, {
        children: [createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "---"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "//..."
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: [createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "const"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " { "
          }), createVNode(_components.span, {
            style: {
              color: "#79B8FF"
            },
            children: "subtitle"
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " ="
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: " await"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " Astro.slots."
          }), createVNode(_components.span, {
            style: {
              color: "#B392F0"
            },
            children: "render"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "("
          }), createVNode(_components.span, {
            style: {
              color: "#9ECBFF"
            },
            children: "'subtitle'"
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: ") } "
          }), createVNode(_components.span, {
            style: {
              color: "#F97583"
            },
            children: "="
          }), createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: " Astro.props;"
          })]
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#6A737D"
            },
            children: "---"
          })
        }), "\n", createVNode(_components.span, {
          class: "line"
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "//..."
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "{subtitle && <p class=\"text-xl text-muted dark:text-slate-400\" set:html={subtitle} />}"
          })
        }), "\n", createVNode(_components.span, {
          class: "line",
          children: createVNode(_components.span, {
            style: {
              color: "#E1E4E8"
            },
            children: "//..."
          })
        })]
      })
    }), "\n", createVNode(_components.p, {
      children: "There’s a lot to wrap your head around, here."
    }), "\n", createVNode(_components.p, {
      children: ["Notice first that ", createVNode(_components.em, {
        children: "subtitle"
      }), " is defined as a prop/argument, but it’s being processed as a slot. Interestingly, prop args and slots seem to be somewhat interchangeable: if the subtitle was just a string, it would simply take that assignment. The main difference is that if you render them independently, you have to call the render with an ", createVNode(_components.em, {
        children: "await"
      }), " modifier."]
    })]
  });
}
function MDXContent(props = {}) {
  const {wrapper: MDXLayout} = props.components || ({});
  return MDXLayout ? createVNode(MDXLayout, {
    ...props,
    children: createVNode(_createMdxContent, {
      ...props
    })
  }) : _createMdxContent(props);
}

const url = "src/data/post/astrowind-template-in-depth.mdx";
const file = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/data/post/astrowind-template-in-depth.mdx";
const Content = (props = {}) => MDXContent({
  ...props,
  components: { Fragment: Fragment, ...props.components, },
});
Content[Symbol.for('mdx-component')] = true;
Content[Symbol.for('astro.needsHeadRendering')] = !Boolean(frontmatter.layout);
Content.moduleId = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/data/post/astrowind-template-in-depth.mdx";
__astro_tag_component__(Content, 'astro:jsx');

export { Content, Content as default, file, frontmatter, getHeadings, url };
