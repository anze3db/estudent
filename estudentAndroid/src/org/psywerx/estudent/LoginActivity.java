package org.psywerx.estudent;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends Activity {

	private Context mContext;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login);
		mContext = this;

		final EditText eUsername = (EditText) findViewById(R.id.eUsername);
		final EditText ePassword = (EditText) findViewById(R.id.ePassword);
		final Button btnConfirm = (Button) findViewById(R.id.btnConfirm);

		btnConfirm.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				if (eUsername.length() == 0) {
					eUsername.setError(getText(R.string.error_required));
					return;
				}
				if (ePassword.length() == 0) {
					ePassword.setError(getText(R.string.error_required));
					return;
				}
				Toast.makeText(mContext, getText(R.string.error_wrongUP), Toast.LENGTH_SHORT).show();
			}
		});
	}
}
