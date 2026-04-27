module.exports = function (eleventyConfig) {
  // Copy assets straight through to the build output
  eleventyConfig.addPassthroughCopy("src/assets");

  return {
    pathPrefix: "/kgb-geocaching/",
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    // Use Nunjucks for both templates and markdown
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
};
