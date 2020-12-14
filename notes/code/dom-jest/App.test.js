import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import userEvent from "@testing-library/user-event";

import App from "./App";

describe("The application", () => {
	test("Should render correctly", () => {
		render(<App />);

		expect(screen.getByText(/the amazing calculator/i)).toBeInTheDocument();
		// screen.debug();
	});
	test("Should be able to use the inputs to calculate that 2 * 3 = 6, and that changing the inputs changes the result", () => {
		render(<App />);

		expect(screen.getByText(/the amazing calculator/i)).toBeInTheDocument();

		//check that there are two inputs, and get them both
		expect(screen.getAllByRole("textbox").length).toBe(2);

		expect(
			screen.getByRole("textbox", { name: "first" })
		).toBeInTheDocument();
		const first = screen.getByRole("textbox", { name: "first" });
		expect(
			screen.getByRole("textbox", { name: "second" })
		).toBeInTheDocument();
		const second = screen.getByRole("textbox", { name: "second" });

		//now enter the values
		userEvent.type(first, "2");
		expect(first.value).toBe("2");

		userEvent.type(second, "3");
		expect(second.value).toBe("3");

		//now get the select
		expect(
			screen.getByRole("combobox", { name: "operation" })
		).toBeInTheDocument();
		const select = screen.getByRole("combobox", { name: "operation" });

		userEvent.selectOptions(select, "*");
		expect(select.value).toBe("*");

		//check - we expect to see a 6 somewhere on the screen
		expect(screen.getByText(/6/)).toBeInTheDocument();

		//part 2 - if we change the value, does the value change?
		userEvent.clear(first);
		userEvent.type(first, "11");
		expect(first.value).toBe("11");

		userEvent.clear(second);
		userEvent.type(second, "9");
		expect(second.value).toBe("9");

		userEvent.selectOptions(select, "-");
		expect(select.value).toBe("-");

		//check the the original result disappeared and was replaced with the new one
		expect(screen.queryByText(/6/)).not.toBeInTheDocument();
		expect(screen.getByText(/2/)).toBeInTheDocument();
	});
});
