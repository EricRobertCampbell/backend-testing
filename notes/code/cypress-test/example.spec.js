describe("Our main application", () => {
	it("Should take an input, display the result, and then display a new result when the inputs change", () => {
		//make the initial visit
		cy.visit("http://localhost:3000/");
		cy.findByText(/the amazing calculator/i).should("exist");

		//now muck about with the options
		cy.findByRole("textbox", { name: "first" })
			.type(6)
			.should("have.value", 6);
		cy.findByRole("textbox", { name: "second" })
			.type(5)
			.should("have.value", "5");
		cy.findByRole("combobox", { name: "operation" })
			.select("*")
			.should("have.value", "*");
		cy.findByText(/30/).should("be.visible");

		//now change the options and see that the result changes as well
		cy.findByRole("textbox", { name: "first" })
			.clear()
			.type(5)
			.should("have.value", 5);
		cy.findByRole("textbox", { name: "second" })
			.clear()
			.type(9)
			.should("have.value", "9");
		cy.findByRole("combobox", { name: "operation" })
			.select("-")
			.should("have.value", "-");
		cy.findByText(/30/).should("not.exist");
		cy.findByText(/-4/).should("be.visible");
	});
});
