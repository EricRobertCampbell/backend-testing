import React, { useState, useEffect } from "react";
import { Form, Text, Select } from "informed";
import { add, subtract, multiply, divide } from "../functions";

function App() {
	const [result, setResult] = useState();
	const handleChange = (formState) => {
		console.log("handleChange called");
		const first = formState.values.first;
		const op = formState.values.op;
		const second = formState.values.second;

		console.log("in handleChange", { first, op, second });

		switch (op) {
			case "+":
				setResult(add(first, second));
				break;
			case "-":
				setResult(subtract(first, second));
				break;
			case "*":
				setResult(multiply(first, second));
				break;
			case "/":
				setResult(divide(first, second));
				break;
			default:
				console.log("Error: you shouldn't be here");
		}
	};
	return (
		<>
			{" "}
			<h1>The Amazing Calculator!</h1>
			<Form>
				{({ formState }) => {
					return (
						<>
							<Text
								aria-label="first"
								field="first"
								onChange={(e) => handleChange(formState)}
							/>
							<Select
								aria-label="operation"
								field="op"
								defaultValue="+"
								onChange={(e) => handleChange(formState)}
							>
								<option value="+">+</option>
								<option value="-">-</option>
								<option value="*">*</option>
								<option value="/">/</option>
							</Select>
							<Text
								aria-label="second"
								field="second"
								onChange={(e) => handleChange(formState)}
							/>
							<span>{` = ${
								result === undefined ? "" : result
							}`}</span>
						</>
					);
				}}
			</Form>
		</>
	);
}

export default App;
