from db.record import Record
from db.cell import Cell
from db.db_session import create_session, global_init
from catcher import tracker, find_imsi
from scapy.all import sniff, UDP


def record_exists(imsi):
    session = create_session()
    if session.query(Record).filter(Record.imsi == imsi).first():
        session.close()
        return True
    else:
        session.close()
        return False


def new_record(imsi, country, brand, operator, lac, cellid, timestamp):
    session = create_session()
    seen = [{"timestamp": timestamp, "LAC": lac, "cell_id": cellid}]
    rec = Record(imsi=imsi, country=country, brand=brand, operator=operator, seen=seen, log_level=0)
    session.add(rec)
    session.commit()
    session.close()


def just_saw_record(imsi, timestamp, lac, cellid):
    session = create_session()
    rec = session.query(Record).filter(Record.imsi == imsi).first()
    rec.seen = rec.seen + [{"timestamp": timestamp, "LAC": lac, "cell_id": cellid}]
    loglevel = rec.log_level
    session.commit()
    session.close()
    if str(loglevel) == "1":
        return True
    return False


def cell_exists(cellid):
    session = create_session()
    if session.query(Cell).filter(Cell.cell_id == cellid).first():
        session.close()
        return True
    else:
        session.close()
        return False


def new_cell(cellid, lac, get_location=False):
    session = create_session()
    if get_location:
        # !!!
        cl = Cell(cell_id=cellid, lac=lac)
    else:
        cl = Cell(cell_id=cellid, lac=lac)
    session.add(cl)
    session.commit()
    session.close()


def process_record(cpt, tmsi1, tmsi2, imsi, imsicountry, imsibrand, imsioperator, mcc, mnc, lac, cell, timestamp,
                   packet=None):
    if not cell_exists(cell):
        new_cell(cell, lac, get_location=True)
    if not record_exists(imsi):
        new_record(imsi, imsicountry, imsibrand, imsioperator, lac, cell, timestamp)
    elif just_saw_record(imsi, timestamp, lac, cell):
        session = create_session()
        rec = session.query(Record).filter(Record.imsi == imsi)
        print("[WARNING] Seen {} named \"{}\" from {} on {} by {}".format(rec.imsi, rec.name, rec.country, rec.brand,
                                                                          rec.operator))
        session.close()


def find_imsi_from_pkt(p):
    global imsitracker
    udpdata = bytes(p[UDP].payload)
    find_imsi(udpdata, imsitracker)


if __name__ == "__main__":
    global_init("db/db.sqlite")
    imsitracker = tracker()
    imsitracker.set_output_function(process_record)

    sniff(iface="lo", filter="port {} and not icmp and udp".format(4729), prn=find_imsi_from_pkt,
          store=0)
