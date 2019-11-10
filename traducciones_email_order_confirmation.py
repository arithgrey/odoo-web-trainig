<div style="margin: 0px; padding: 0px;">
                    % set street_name = object.partner_id.street_name if object.partner_id.street_name else ""
                    % set street_number = "%s %s"| format("#", object.partner_id.street_number ) if object.partner_id.street_number else ""
                    % set street_number2 = object.partner_id.street_number2 if object.partner_id.street_number2 else ""
                    % set l10n_mx_edi_colony = object.partner_id.l10n_mx_edi_colony if object.partner_id.l10n_mx_edi_colony else ""
                    % set l10n_mx_edi_locality = object.partner_id.l10n_mx_edi_locality if object.partner_id.l10n_mx_edi_locality else ""
                    % set zip = "%s %s"| format("C.P.", object.partner_id.zip ) if object.partner_id.zip else ""
                    % set state_name = object.partner_id.state_id.name if object.partner_id.state_id.name else ""
                    % set country_name = "%s %s"| format("," , object.partner_id.country_id.name ) if object.partner_id.country_id.name else ""
                    % set invoice_street_name = object.partner_invoice_id.street_name if object.partner_invoice_id.street_name else ""
                    % set invoice_street_number = "%s %s"| format("#", object.partner_invoice_id.street_number) if object.partner_invoice_id.street_number else ""

                    % set invoice_street_number2 = object.partner_invoice_id.street_number2 if object.partner_invoice_id.street_number2 else ""
                    % set invoice_l10n_mx_edi_colony = object.partner_invoice_id.l10n_mx_edi_colony if object.partner_invoice_id.l10n_mx_edi_colony else ""
                    % set invoice_l10n_mx_edi_locality = object.partner_invoice_id.l10n_mx_edi_locality if object.partner_invoice_id.l10n_mx_edi_locality else ""
                    % set invoice_zip = "%s %s"| format("C.P.", object.partner_invoice_id.zip ) if object.partner_invoice_id.zip else ""
                    % set invoice_state_name = object.partner_invoice_id.state_id.name if object.partner_invoice_id.state_id.name else ""
                    % set invoice_country_name = "%s %s"| format(",", object.partner_invoice_id.country_id.name ) if object.partner_invoice_id.country_id.name else ""
                    % set ticket_url = object.ticket_url if object.ticket_url else ""

                    % set url = "https://benandfrank.com"
                    % set url_logo_benandfrank = "https://cdn.shopify.com/s/files/1/0838/5577/t/67/assets/header_logo_black_2x.png?397132"
                    % set website_link = "{0}".format(url)
                    % set facebook_link = object.partner_id.company_id.social_facebook
                    % set instagram_link = object.partner_id.company_id.social_instagram
                    % set currency_id = object.pricelist_id.currency_id
                    <body>
                        <div>
                            <div class="text-center" style="text-align: center;">
                                <a href="http://www.benandfrank.com/">
                                    <img align="center" src="${url_logo_benandfrank}" class="logo_bnf" style="width: 195.5px;height: 27px;"/>
                                </a>
                            </div>
                            <div>
                                <hr style="background-color: #000;"/>
                            </div>
                            <div style="margin-top: 30px;margin-bottom:20px;">
                                <p class="text-order" style="font-size: 21px!important;color: #000000;font-family: Arial;font-weight: bold;font-stretch: normal;font-style: normal;line-height: 1.14;letter-spacing: normal;text-align: right;">
                                        Número de orden
                                        ${object.name}
                                </p>
                            </div>
                            <div class="top">
                                <p class="date_delivery" style="font-size: 14px;color: #666666!important;line-height: 1.43;text-align: right;font-weight: bold;margin:0px!important;">
                                    Fecha de entrega máxima: 10 días hábiles
                                </p>
                                <p class="date_delivery_description" style="font-size: 14px;color: #666666!important;text-align: right;margin:0px!important;">
                                    (Si ya pagaste y mandaste tu receta)
                                </p>
                            </div>
                            <hr style="background-color: #000;margin-top: 30px;"/>
                            <div style="margin-top: 30px;">
                                <p class="text-capitalize" style="font-size: 14px;color: #000;text-transform: capitalize;">
                                    Hola ${object.partner_id.name},
                                </p>
                            </div>
                            <div>
                                <p style="font-size: 14px;color: #000;">
                                    ¡Qué bien que compraste tus Ben &amp; Frank!
                                </p>
                            </div>
                            <div class="bottom" style="margin-bottom: 30px;margin-top: 30px;">
                                <h3 class="text-uppercase" style="width: 409px;height: 20px;font-family: Arial;font-size: 22px;font-weight: bold;font-stretch: normal;font-style: normal;line-height: 1.18;letter-spacing: 1.1px;text-align: left;color: #000000;text-transform: uppercase;">
                                    Detalles de tu orden:
                                </h3>
                            </div>
                            <div>
                                <table width="100%" style="width: 100%;">
                                    % if object.order_line:
                                        % for line in object.order_line:
                                            <tr valign="top">
                                                <td style="width: 25%;padding-top: 30px;">
                                                    % if line.is_spectacle:
                                                        <img src="/product/combination/image/${line.product_id.id}" style="max-width: 100%;height: auto;"/>
                                                    %else
                                                        <img src="/web/image/product.product/${line.product_id.id}" style="max-width: 100%;height: auto;"/>
                                                    %endif
                                                </td>
                                                <td style="padding-top: 30px;padding-left: 5%;">
                                                    <h2 style="font-family: Arial;font-size: 16px;font-weight: bold;font-stretch: normal;font-style: normal;line-height: 1.13;letter-spacing: normal;text-align: left;color: #000000;">
                                                        ${(line.product_uom_qty) | int}
                                                    </h2>
                                                </td>
                                                <td style="padding-top: 30px;padding-left: 10%;" class="desglose-producto">
                                                        % set product = line.product_id
                                                        <h3 style="text-transform: uppercase;font-family: Arial;font-size: 16px;font-weight: bold;font-stretch: normal;font-style: normal;line-height: 1.13;letter-spacing: normal;text-align: left;color: #000000;">
                                                            ${product.name}
                                                        </h3>
                                                        % if product.get_lens_frame():
                                                            % set frame_attribute = product.get_lens_frame().name
                                                            <p style="font-size: 14px;color: #000;margin:0px;">
                                                                - ${frame_attribute}
                                                            </p>
                                                        %endif

                                                        % if line.is_spectacle:
                                                            % if product.get_lens_graduation():
                                                                <p style="font-size: 14px;color: #000;margin:0px;">
                                                                    - Con graduación
                                                                </p>
                                                            %else
                                                                <p style="font-size: 14px;color: #000;margin:0px;">
                                                                    - Sin graduación
                                                                </p>
                                                            %endif
                                                            % if product.get_lens_treatment():
                                                                % set lens_treatment =  product.get_lens_treatment().name
                                                                <p style="font-size: 14px;color: #000;margin:0px;">
                                                                    - ${lens_treatment}
                                                                </p>
                                                            %endif
                                                        %endif
                                                </td>
                                                <td style="padding-top: 30px;">
                                                    <p style="font-size: 16px;                                                             font-weight: normal;                                                             font-stretch: normal;                                                             line-height: 1.13;                                                             letter-spacing: normal;                                                             text-align: right;                                                             color: #000;">
                                                        ${format_amount(line.price_total, currency_id)}
                                                    </p>
                                                </td>
                                            </tr>
                                    % endfor
                                % endif
                                </table>
                            </div>
                            <div>
                                <table style="width:100%; text-align: right;">
                                    <tr>
                                        <td>
                                            <p style="font-size: 18px;">
                                                <span style="color:#000;">
                                                    Subtotal:
                                                </span>
                                                <span style="font-weight:bold;color:#000;">
                                                    ${format_amount(object.amount_undiscounted, currency_id)}
                                                </span>
                                            </p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <p style="font-size: 18px;color: #000;">
                                                <span style="color:#000;">
                                                    Total:
                                                </span>
                                                <span style="font-weight:bold;">
                                                    ${format_amount(object.amount_total, currency_id)}
                                                </span>
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            <hr/>
                            <table style="width: 100%;margin-top:30px;margin-bottom:30px;">
                                <tr>
                                    <td>
                                        <table style="width: 100%;">
                                            <tr>
                                                <td>
                                                    <div>
                                                        <h4 style="font-family:Arial;font-weight:bold;color:#000;display:block;font-size:14px;font-style:normal;font-weight:italic;line-height:110%;letter-spacing:normal;margin:0;margin-bottom:10px;text-align:left">
                                                            Dirección de Pago:
                                                        </h4>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${invoice_street_name }
                                                        ${invoice_street_number }
                                                        ${invoice_street_number2 }
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${invoice_l10n_mx_edi_colony }
                                                        ${invoice_l10n_mx_edi_locality }
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${invoice_zip }
                                                        ${invoice_state_name }
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${invoice_country_name }
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td style="width:10%;">
                                    </td>
                                    <td style="width:45%;">
                                        <table style="width:100%;margin:0 auto">
                                            <tr>
                                                <td>
                                                    <div>
                                                        <h4 style="font-family:Arial;font-weight:bold;color:#000;display:block;font-size:14px;font-style:normal;font-weight:italic;line-height:110%;letter-spacing:normal;margin:0;margin-bottom:10px;text-align:left">
                                                            Dirección de Envío:
                                                        </h4>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${street_name }
                                                        ${street_number }
                                                        ${street_number2 }
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${l10n_mx_edi_colony }
                                                        ${l10n_mx_edi_locality }
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                    ${zip }
                                                    ${state_name }
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p style="font-size: 14px;color: #666666;">
                                                        ${country_name }
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            <hr/>
                            <div style="margin-top: 50px;">
                                <table style="text-align:center;width:100%;">
                                    <tr>
                                        <td>
                                            <p style="   font-size: 14px;   text-align: center;   color: #000000;">
                                                Si tu información es incorrecta, avísanos (a menos que quieras regalárselos a tu vecino).
                                            </p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <p style="   font-size: 14px;   text-align: center;   color: #000000;">
                                                Sabemos que ya los quieres usar, así que prometemos que nos vamos a apurar.
                                            </p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding-top: 40px;padding-bottom: 30px;">
                                            % set path_download = ""
                                            % set invoice_link =""
                                            % if object.access_token:
                                                %set path_download= "?access_token="+ object.access_token + "&amp;report_type=pdf&amp;download=true"
                                            %endif
                                            % for invoice in object.invoice_ids:

                                               % set invoice_link = "%s%s%s%s"| format(object.get_base_url() , '/my/invoices/', invoice.id,  path_download)

                                            % endfor

                                            <a href="" style="                                                                   box-shadow: 3px 3px 0 0 rgba(0, 0, 0, 0.16);                                                                   border: solid 2px #ffffff;                                                                   background-color: #000000;                                                                   font-style: normal;                                                                   font-stretch: normal;                                                                   line-height: 1.15;                                                                   letter-spacing: 2px;                                                                   text-align: center;                                                                   color: #ffffff;                                                                   padding: 10px 30px 10px 30px;                                                                   text-transform: uppercase;                                                                   font-weight:bold;                                                                 ">
                                                ¿Dónde viene mi pedido?
                                            </a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding-top: 10px;padding-bottom: 30px;">
                                            <a href="" style="font-family: Arial;                                                                   font-size: 16px;                                                                   font-weight: bold;                                                                   font-stretch: normal;                                                                   font-style: normal;                                                                   line-height: 1.25;                                                                   letter-spacing: normal;                                                                   text-align: center;                                                                   color: #000000;                                                                   text-decoration:underline;">

                                                <span style="text-transform:capitalize;">
                                                    Factura
                                                </span>
                                                tu pedido
                                            </a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="text-align:center;">
                                            <p style="font-size:14px;color:#000;width:80%;margin:0 auto;">
                                                Si aún no tenemos tu receta...responde a este mail o escríbenos a hola@benandfrank.com y adjunta la imagen de tu receta en el correo.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            <hr style="margin-top: 50px;"/>
                            <div style="margin:0 auto;text-align: center;margin-top:30px;">
                                <h4 style="                                           font-size: 11px;                                           font-weight: bold;                                           font-style: normal;                                           font-stretch: normal;                                           line-height: 1.13;                                           letter-spacing: 1.6px;                                           text-align: center;                                           color: #000000;text-transform:uppercase;                                           ">
                                        ¿Tienes dudas?
                                </h4>
                            </div>
                            <div style="margin-top: 30px;margin-bottom: 30px;">
                                <p style="margin:0;padding-bottom:0;text-align: center;font-size:9px;text-transform: uppercase;color: #000000;letter-spacing: 1.4px;">
                                    Responde a este correo y nos pondremos las pilas para contestarte lo más rápido posible.
                                </p>
                                <p style="margin:0;padding-bottom:0;text-align: center;font-size:9px;text-transform: uppercase;color: #000000;letter-spacing: 1.4px;margin-top: 10px;">
                                    Llámanos al (55) 1205 1050 de Lunes a Viernes 9 a.m. a 7 p.m.
                                </p>
                            </div>
                            <hr/>
                            <table width="100%" border="0" cellspacing="0" cellpading="0" style="width: 100%;margin-top:30px">
                                <tr>
                                    <td align="center" class="social-icons" style="align-items: center;margin: 30px auto;">
                                        <a href="${ website_link }" style="color: inherit;font-weight: bold;text-decoration: none;padding: 0 20px !important;">
                                            <img class="social-image" src="https://i.postimg.cc/CdxwX6v9/website-icon.png" alt="go to website" style="height: 24px;"/>
                                        </a>
                                        <a href="${ instagram_link }" style="color: inherit;font-weight: bold;text-decoration: none;padding: 0 20px !important;">
                                            <img class="social-image" src="https://i.postimg.cc/F1Ch4g8z/instagram-icon.png" alt="instagram" style="height: 24px;"/>
                                        </a>
                                        <a href="${ facebook_link }" style="color: inherit;font-weight: bold;text-decoration: none;padding: 0 20px !important;">
                                            <img class="social-image" src="https://i.postimg.cc/0KjxSbM9/facebook-icon.png" alt="facebook" style="height: 24px;"/>
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <div style="margin:0 auto;text-align: center;">
                                <div style="margin:0;padding-bottom:0;text-align: center;margin-top: 10px;">
                                    <p style="font-size: 10px;color: #000;">
                                        Ben &amp; Frank
                                    </p>
                                </div>
                            </div>
                        </div>
                    </body>
                </div>
            