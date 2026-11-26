1. Topic
   Dictionary Set-Difference / Membership Lookup, String Parsing & State Aggregation
   This problem tests safe hash-table lookups across mismatched key sets, extracting structured metadata (units) from composite string keys, and separating pure domain computation from I/O side effects (especially critical once you apply the Bonus Challenge). Naive brute force—like nested loops matching keys across two lists or assuming both dictionaries always share identical keys—breaks immediately on missing inventory items (KeyError) or degrades from $O(N)$ to $O(N^2)$.
2. Concepts
   Left-Outer Join Semantics over Dictionaries: par*levels is the authoritative set of required ingredients ($K*{\text{par}}$). current_stock ($K*{\text{stock}}$) may be a subset of $K*{\text{par}}$ (items completely out of stock aren't even recorded as 0 in current*stock), or may contain extra items not needed tonight ($K*{\text{stock}} \setminus K*{\text{par}}$). Iterating over par_levels and defaulting missing stock lookups to 0 enforces a left-join invariant without mutating the caller's current_stock dictionary.
   Key-Encoded Schema & Suffix Parsing: The dictionary keys encode two pieces of data: <ingredient_name>*<unit>. Splitting from the right on the last underscore (rsplit("_", 1)) isolates the unit suffix (kg, liters) even when the ingredient name itself contains underscores (e.g., chicken_breast_kg -> ("chicken_breast", "kg")). Naive split("_") breaks on multi-word ingredients.
   IEEE 754 Floating-Point Subtraction & Display Formatting: Subtracting floats like par - current can produce binary representation artifacts (1.5000000000000002 or trailing .0 when subtracting floats that yield whole numbers). You must decide how to format clean integer vs. fractional amounts.
   Separation of Computation vs. Presentation (Bonus Requirement): A reusable function generate_prep_list(par, stock) should return structured data (or a formatted report string) rather than hardcoding print() side effects inside business logic—making it testable with pytest without capturing stdout.

3. Algorithmic Reading & Problem Decomposition
   Inputs:
   par*levels: mapping {ingredient_key: numeric_required_amount} (e.g., {"onions_kg": 10, "garlic_kg": 2.0, ...}).
   current_stock: mapping {ingredient_key: numeric_available_amount} where keys present in par_levels may be absent (implied quantity 0).
   Outputs:
   Header banner (--- TONIGHT'S KITCHEN PREP LIST ---).
   One status line per ingredient in par_levels, preserving par_levels insertion order:
   Deficit (available < required): <ingredient_key>: NEED <deficit> <unit>
   Sufficient (available >= required): <ingredient_key>: OK
   Footer divider (-----------------------------------) and summary count (Total items to prep/order: <count>).
   Constraints & Spec Gaps (Challenge These):
   Unit extraction: Does every key in par_levels strictly end with *<unit>? What if a key has no underscore?
   Negative values: Can current_stock or par_levels ever be negative? If par_levels has 0, 0 >= 0 evaluates to OK.
   Extra keys in current_stock: Items in the walk-in cooler that are not in tonight's par_levels must be ignored, not flagged.
   Zero-deficit edge case: When available == required, the status is OK and the item does not increment the prep/order counter.
   Subproblems:
   Unit Extraction: Parse <unit> from the suffix of each par_levels key.
   Safe Stock Retrieval: Look up available in current_stock with a fallback default of 0 (without mutating current_stock).
   Threshold Evaluation & Deficit Calculation: Compare available against required; compute deficit = required - available when available < required, and increment the attention counter.
   Report Assembly & Output: Format individual lines, header, footer, and total count cleanly.

4. Top-Down Method (main + helper)
   main()
   Role: Data setup (defining/loading par*levels and current_stock), invoking the reusable prep-list generator, and emitting the final report to stdout.
   Contract:
   Initialize par_levels and current_stock (testing both the baseline case and the bonus case where "heavy_cream_liters" is absent from current_stock).
   Call generate_prep_list(par_levels, current_stock).
   Print the returned report (or unpack returned structured items + count and print them).
   helper: generate_prep_list(par, stock) (plus optional small unit-parsing helper)
   Parameters:
   par: dict[str, int | float] — required minimum quantities keyed by <name>*<unit>.
   stock: dict[str, int | float] — current inventory quantities (may omit keys present in par).
   Return Value: Either a formatted multi-line str ready to print, or a structured result tuple (status*lines: list[str], items_needed_count: int) that main() prints. (Returning data instead of printing inside the function makes the function genuinely reusable and unit-testable.)
   Termination / Base / Transition Logic:
   Initialize lines list (with header) and attention_count = 0.
   Iterate once through each (item_key, required_qty) in par.items():
   Retrieve available_qty from stock defaulting to 0 if item_key is missing.
   If available_qty < required_qty:
   Extract unit from the trailing *<unit> segment of item_key.
   Compute missing_qty = required_qty - available_qty (normalizing float precision if needed).
   Append f"{item_key}: NEED {missing_qty} {unit}" to lines and increment attention_count.
   Else (available_qty >= required_qty):
   Append f"{item_key}: OK" to lines.
   Append footer divider and f"Total items to prep/order: {attention_count}", then return.

5. Complexity:
   Time complexity: $O(N)$ where $N = \text{len}(par)$—one linear pass over par, with amortized $O(1)$ dictionary lookups into stock and $O(L)$ suffix split on short key strings of length $L$.
   Space complexity: $O(N)$ to store the generated output lines/report (and $O(1)$ extra auxiliary state beyond the output buffer, without copying or mutating stock).
6. Note to Take Away
   Never assume two dictionaries in the real world have synchronized keys, and never assume identifiers are atomic strings. Using safe default lookups (.get(key, 0)) eliminates an entire class of KeyError crashes without mutating input state, and splitting composite keys from the right (rsplit("\_", 1)) prevents multi-word names like chicken_breast_kg from breaking your parser.
