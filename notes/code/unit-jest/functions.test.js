import { add, subtract, multiply, divide } from "./functions";
describe("The 'add' function", () => {
	it("Should correctly sum up two numbers", () => {
		expect(add(2, 3)).toBe(5);
		expect(add(2.1, 4)).toBe(6.1);
		expect(add(-1, 1)).toBe(0);
	});
	it("Should throw an error if you pass in a non-number", () => {
		expect(() => add("2", "3")).toThrow("You need to pass in a number!"); //note the additional function here!
	});
	it("Should return `undefined` if you miss an argument", () => {
		expect(add()).toBeUndefined();
		expect(add(1)).toBeUndefined();
	});
});
