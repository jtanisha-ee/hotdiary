/*
 * Copyright (c) 1999 HotDiary, Inc. All Rights Reserved.
 *
 * HOTDIARY reserves the right to distribute this software and license.
 * THIS SOFTWARE MAY NOT BE DUPLICATED OR COPIED IN ANY FORM by user
 * without the permission of HOTDIARY.
 * ALL EXPRESS OR IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY
 * IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR
 * NON-INFRINGEMENT, ARE HEREBY EXCLUDED. HOTDIARY AND ITS LICENSORS SHALL NOT BE
 * LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING
 * THE SOFTWARE. IN NO EVENT WILL HOTDIARY OR ITS LICENSORS BE LIABLE FOR ANY
 * LOST REVENUE, PROFIT OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL,
 * INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY
 * OF LIABILITY, ARISING OUT OF THE USE OF OR INABILITY TO USE SOFTWARE, EVEN IF
 * HOTDIARY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 *
 * This software is not designed or intended for use in on-line control of
 * aircraft, air traffic, aircraft navigation or aircraft communications; or in
 * the design, construction, operation or maintenance of any nuclear
 * facility. Licensee represents and warrants that it will not use or
 * redistribute the Software for such purposes.
 */

package COM.hotdiary.eventfeed.hdif;

public interface EFServer extends java.rmi.Remote {
// some example params, needs to change for real thing
    public void feedEvent(String title, String desc) throws java.rmi.RemoteException;
    public String authUser(HDLogin lg) throws java.rmi.RemoteException;
    public String setEvent(HDEvent ev) throws java.rmi.RemoteException;
}
