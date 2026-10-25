import { describe, expect, it } from "vitest";
import { safeSlug } from "./utils";

describe("safeSlug", () => {
  it("converts a title into a safe filename slug", () => {
    expect(safeSlug("Weather API: Current Conditions")).toBe("weather-api-current-conditions");
  });
  it("returns a fallback for empty or non-ASCII-only titles", () => {
    expect(safeSlug("!!!")).toBe("documentation");
  });
});
