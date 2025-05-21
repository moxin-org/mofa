import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const metadataDefinition = () =>
  z
    .object({
      title: z.string().optional(),
      ignoreTitleTemplate: z.boolean().optional(),

      canonical: z.string().url().optional(),

      robots: z
        .object({
          index: z.boolean().optional(),
          follow: z.boolean().optional(),
        })
        .optional(),

      description: z.string().optional(),

      openGraph: z
        .object({
          url: z.string().optional(),
          siteName: z.string().optional(),
          images: z
            .array(
              z.object({
                url: z.string(),
                width: z.number().optional(),
                height: z.number().optional(),
              })
            )
            .optional(),
          locale: z.string().optional(),
          type: z.string().optional(),
        })
        .optional(),

      twitter: z
        .object({
          handle: z.string().optional(),
          site: z.string().optional(),
          cardType: z.string().optional(),
        })
        .optional(),
    })
    .optional();

const postCollection = defineCollection({
  type: 'content',
  schema: z.object({
    publishDate: z.date().optional(),
    updateDate: z.date().optional(),
    draft: z.boolean().optional(),

    title: z.string(),
    excerpt: z.string().optional(),
    image: z.string().optional(),

    category: z.string().optional(),
    tags: z.array(z.string()).optional(),
    author: z.string().optional(),

    metadata: metadataDefinition(),
  }),
});

// 定义单语言内容结构
const languageContentSchema = z.object({
  title: z.string().optional(),
  description: z.string().optional(),
});

// 定义单语言Hero部分结构
const languageHeroSchema = z.object({
  title: z.string().optional(),
  subtitle: z.string().optional(),
  actions: z.array(
    z.object({
      text: z.string(),
      href: z.string(),
      variant: z.string().optional(),
      icon: z.string().optional(),
      target: z.string().optional(),
    })
  ).optional(),
});

// 定义单语言Core部分结构
const languageCoreSchema = z.object({
  title: z.string().optional(),
  values: z.string().optional(),
});

// 定义单语言Features部分结构
const languageFeaturesSchema = z.object({
  tagline: z.string().optional(),
  title: z.string().optional(),
  subtitle: z.string().optional(),
  items: z.array(
    z.object({
      title: z.string(),
      description: z.string(),
      icon: z.string().optional(),
    })
  ).optional(),
});

// 定义单语言Design部分结构
const languageDesignSchema = z.object({
  tagline: z.string().optional(),
  title: z.string().optional(),
  content: z.object({
    title: z.string().optional(),
    description: z.string().optional(),
  }).optional(),
  items: z.array(
    z.object({
      title: z.string(),
      description: z.string(),
    })
  ).optional(),
});

// 定义单语言Patterns部分结构
const languagePatternsSchema = z.object({
  tagline: z.string().optional(),
  title: z.string().optional(),
  subtitle: z.string().optional(),
  items: z.array(
    z.object({
      title: z.string(),
      description: z.string(),
      icon: z.string().optional(),
    })
  ).optional(),
});

// 定义单语言Quickstart部分结构
const languageQuickstartSchema = z.object({
  title: z.string().optional(),
  steps: z.array(
    z.object({
      title: z.string(),
      description: z.string().optional(),
      icon: z.string().optional(),
    })
  ).optional(),
});

// 定义单语言FAQ部分结构
const languageFaqSchema = z.object({
  tagline: z.string().optional(),
  title: z.string().optional(),
  subtitle: z.string().optional(),
  items: z.array(
    z.object({
      title: z.string(),
      description: z.string(),
    })
  ).optional(),
});

// 定义单语言CTA部分结构
const languageCtaSchema = z.object({
  title: z.string().optional(),
  subtitle: z.string().optional(),
  actions: z.array(
    z.object({
      text: z.string(),
      href: z.string(),
      variant: z.string().optional(),
      icon: z.string().optional(),
      target: z.string().optional(),
    })
  ).optional(),
});

// 定义网站内容集合 - 支持多语言结构
const siteContentCollection = defineCollection({
  type: 'content',
  schema: z.object({
    // 多语言元数据
    metadata: z.record(z.enum(['en', 'zh']), languageContentSchema).optional(),
    
    // 多语言首页各部分内容
    hero: z.record(z.enum(['en', 'zh']), languageHeroSchema).optional(),
    core: z.record(z.enum(['en', 'zh']), languageCoreSchema).optional(),
    features: z.record(z.enum(['en', 'zh']), languageFeaturesSchema).optional(),
    design: z.record(z.enum(['en', 'zh']), languageDesignSchema).optional(),
    patterns: z.record(z.enum(['en', 'zh']), languagePatternsSchema).optional(),
    quickstart: z.record(z.enum(['en', 'zh']), languageQuickstartSchema).optional(),
    faq: z.record(z.enum(['en', 'zh']), languageFaqSchema).optional(),
    cta: z.record(z.enum(['en', 'zh']), languageCtaSchema).optional(),
    
    // 多语言导航和页脚翻译
    nav: z.record(z.enum(['en', 'zh']), z.record(z.string(), z.string())).optional(),
    footer: z.record(z.enum(['en', 'zh']), z.record(z.string(), z.string())).optional(),
  }),
});

// 确保类型系统知道我们支持的集合
export const collections = {
  post: postCollection,
  site: siteContentCollection,
};
