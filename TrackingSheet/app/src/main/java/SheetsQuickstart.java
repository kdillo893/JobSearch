
/**
 * sheets tool gleaned from https://developers.google.com/sheets/api/quickstart/java
 *
 * modified in place to point to my own sheet and add rows at blank space.
 */

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.Json;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.sheets.v4.Sheets;
import com.google.api.services.sheets.v4.SheetsRequest;
import com.google.api.services.sheets.v4.SheetsRequestInitializer;
import com.google.api.services.sheets.v4.Sheets.Spreadsheets.Values.Append;
import com.google.api.services.sheets.v4.SheetsScopes;
import com.google.api.services.sheets.v4.model.AppendValuesResponse;
import com.google.api.services.sheets.v4.model.SheetProperties;
import com.google.api.services.sheets.v4.model.ValueRange;

public class SheetsQuickstart {
    private static final String APPLICATION_NAME = "Job Search Sheet Sync";
    private static final JsonFactory JSON_FACTORY = GsonFactory.getDefaultInstance();
    private static final String TOKENS_DIRECTORY_PATH = "tokens";

    /**
     * Global instance of the scopes required by this quickstart.
     * If modifying these scopes, delete your previously saved tokens/ folder.
     */
    private static final List<String> SCOPES = Collections.singletonList(SheetsScopes.SPREADSHEETS);
    private static final String CREDENTIALS_FILE_PATH = "credentials.json";

    /**
     * Creates an authorized Credential object.
     *
     * @param HTTP_TRANSPORT The network HTTP Transport.
     * @return An authorized Credential object.
     * @throws IOException If the credentials.json file cannot be found.
     */
    private static Credential getCredentials(final NetHttpTransport HTTP_TRANSPORT)
            throws IOException {
        // Load client secrets.
        // InputStream in = new FileInputStream(CREDENTIALS_FILE_PATH);
        InputStream in = SheetsQuickstart.class.getResourceAsStream(CREDENTIALS_FILE_PATH);
        if (in == null) {
            throw new FileNotFoundException("Resource not found: " + CREDENTIALS_FILE_PATH);
        }

        System.out.println("credentials found; " + CREDENTIALS_FILE_PATH);

        // //lets test this by reading the creds...
        // byte[] bbuff = new byte[1024];
        // int len = in.read(bbuff);
        //
        // while (len != -1) {
        // System.out.write(bbuff, 0, len);
        // len = in.read(bbuff);
        // }
        // System.out.println();
        //
        // in.close();
        //
        // in = SheetsQuickstart.class.getResourceAsStream(CREDENTIALS_FILE_PATH);

        GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(in));

        // Build flow and trigger user authorization request.
        GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(
                HTTP_TRANSPORT, JSON_FACTORY, clientSecrets, SCOPES)
                .setDataStoreFactory(new FileDataStoreFactory(new java.io.File(TOKENS_DIRECTORY_PATH)))
                .setAccessType("offline")
                .build();
        LocalServerReceiver receiver = new LocalServerReceiver.Builder().setPort(8888).build();
        return new AuthorizationCodeInstalledApp(flow, receiver).authorize("user");
    }

    /**
     * fire off row update given args, each arg entry is sequence column data (A to
     * I)
     */
    public static void main(String... args) throws IOException, GeneralSecurityException {

        // Build a new authorized API client service.
        final NetHttpTransport HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();

        Credential googleCreds = getCredentials(HTTP_TRANSPORT);
        final String spreadsheetId = "1JPKxB2MFNG3DMxOaQy_hUE5cMZfvL2e7UQwqirP35gw";

        // test read
        final String range = "2024 Searches!A2:H2";
        getRowInJobSearches(HTTP_TRANSPORT, googleCreds, spreadsheetId, range);

        // try doing my own add row thing.
        List<Object> row1 = new ArrayList<>();
        row1.add("Applied");
        row1.add("TestJob");
        row1.add("TestCompany");
        row1.add("Chicago, IL");
        row1.add(new Date().toString());
        row1.add(new Date().toString());
        row1.add("Notes here");

        appendRowToJobSearches(HTTP_TRANSPORT, googleCreds, spreadsheetId, row1);
    }

    public static void getRowInJobSearches(final HttpTransport httpTransport, final Credential credential,
            final String sheetId, final String range) throws IOException {

        Sheets service = new Sheets.Builder(httpTransport, JSON_FACTORY, credential)
                .setApplicationName(APPLICATION_NAME)
                .build();

        ValueRange response = service.spreadsheets().values()
                .get(sheetId, range)
                .execute();

        List<List<Object>> values = response.getValues();
        if (values == null || values.isEmpty()) {
            System.out.println("No data found.");
        } else {
            System.out.println("Status, Role Title, Company Name, Location, Date Apply, Date Respond, Notes");
            for (List<Object> row : values) {
                // just print the row for now
                System.out.printf("%s\n", row.toString());
            }
        }

        System.out.println();
    }

    public static void appendRowToJobSearches(HttpTransport HTTP_TRANSPORT, Credential credential,
            final String sheetId, List<Object> newRowValues)
            throws GeneralSecurityException, IOException {

        final String range = "2024 Searches";

        Sheets service = new Sheets.Builder(HTTP_TRANSPORT, JSON_FACTORY, credential)
                .setApplicationName(APPLICATION_NAME).build();

        // ValueRange for body
        List<List<Object>> myRange = new ArrayList<>(new ArrayList<>());

        myRange.add(newRowValues);

        ValueRange toAppend = new ValueRange();
        toAppend.setValues(myRange);

        // make the "request" object with above as body, adding parameters
        Append appendReq = service.spreadsheets().values().append(sheetId, range, toAppend);

        // parameters for append values request
        appendReq.setValueInputOption("USER_ENTERED");
        appendReq.setInsertDataOption("INSERT_ROWS");
        // optional, I wanna see what I inserted.
        appendReq.setIncludeValuesInResponse(true);

        AppendValuesResponse resp = appendReq.execute();

        if (resp == null) {
            System.out.println("uh oh bad response");
            return;
        }

        // out the response for now.
        System.out.println(resp.toString());
    }

    /** todo: I want to try making auth connection without the google library */
    public static void rawAPIUpdateSheet(Json query) throws GeneralSecurityException, IOException {

    }
}
