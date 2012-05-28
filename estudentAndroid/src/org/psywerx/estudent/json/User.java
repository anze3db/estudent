package org.psywerx.estudent.json;

public class User {
	protected String surname;
	protected String name;
	protected String errors;
	protected boolean login;
	protected int numTries;
	
	public boolean getLogin() {
		return login;
	}
	public void setLogin(boolean login) {
		this.login = login;
	}
	public String getErrors() {
		return errors;
	}
	public String getName() {
		return name;
	}
	public int getNumTries() {
		return numTries;
	}
	public String getSurname() {
		return surname;
	}
	public void setErrors(String errors) {
		this.errors = errors;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setNumTries(int numTries) {
		this.numTries = numTries;
	}
	public void setSurname(String surname) {
		this.surname = surname;
	}
	
}
